# Helm chart - pagopa-qa-superset

Umbrella chart per il deploy su Kubernetes/AKS di Apache Superset customizzato pagoPA.

Non ridefinisce i template di Superset: dichiara come dipendenza il
[chart upstream Apache Superset](https://github.com/apache/superset/tree/master/helm/superset)
e ne sovrascrive i values. L'upgrade a una nuova versione upstream e' quindi un bump
di versione in `Chart.yaml` + `helm dependency update`.

## Struttura

```
helm/
├── Chart.yaml         # dependency: superset 0.22.4 (appVersion 6.1.0)
├── values.yaml        # configurazione comune a tutti gli ambienti
├── values-dev.yaml    # override ambiente DEV
├── templates/         # eventuali risorse aggiuntive pagoPA (al momento vuoto)
└── README.md
```

Tutti i values del chart upstream vanno annidati sotto la chiave `superset:`.
Riferimento completo delle opzioni:
<https://github.com/apache/superset/blob/master/helm/superset/README.md>

## Scelte di deploy

| Componente | Scelta |
|---|---|
| Metadata DB | Azure Database for PostgreSQL (`postgresql.enabled: false`) |
| Cache / broker Celery | Azure Cache for Redis, TLS su 6380 (`redis.enabled: false`) |
| Immagine | build custom di questo repo su ACR (`pagopadcommonacr`) |
| Segreti | secret Kubernetes esterno, montato via `envFromSecrets` |
| Celery beat / flower / websockets / MCP | disabilitati |

### Gestione dei segreti

Il chart upstream genera da solo il secret `<release>-superset-env` con i valori **non
sensibili** (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_NAME`, `REDIS_HOST`, ...).

I segreti veri arrivano da un secret creato **fuori da Helm** (External Secrets Operator
o Azure Key Vault CSI driver) e referenziato in `superset.envFromSecrets`. Essendo
montato dopo, le sue chiavi vincono su quelle generate dal chart.

Secret atteso: `<release>-secrets` (es. `pagopa-qa-superset-secrets`), con le chiavi

| Chiave | Contenuto |
|---|---|
| `DB_PASS` | password PostgreSQL |
| `REDIS_PASSWORD` | access key Redis |
| `SUPERSET_SECRET_KEY` | chiave di cifratura Superset (`openssl rand -base64 42`) |

> ⚠️ La `SUPERSET_SECRET_KEY` non va mai ruotata a caldo senza prima eseguire
> `superset re-encrypt-secrets`: le credenziali dei database registrati in Superset
> sono cifrate con quella chiave.

## Prerequisiti

- Helm >= 3.8
- accesso al cluster AKS e al namespace di destinazione
- il secret esterno descritto sopra gia' presente nel namespace

## Uso

Scaricare/aggiornare la dipendenza upstream (crea `charts/` e `Chart.lock`):

```bash
helm dependency update ./helm
```

Verificare il render senza applicare nulla:

```bash
helm template pagopa-qa-superset ./helm \
  -f helm/values.yaml \
  -f helm/values-dev.yaml \
  --set superset.init.adminUser.password='<password>'
```

Deploy su DEV:

```bash
helm upgrade --install pagopa-qa-superset ./helm \
  -n <namespace> --create-namespace \
  -f helm/values.yaml \
  -f helm/values-dev.yaml \
  --set superset.image.tag=<build-id> \
  --set superset.init.adminUser.password='<password>'
```

Rollback:

```bash
helm rollback pagopa-qa-superset -n <namespace>
```

## Aggiornare il chart upstream

1. Controllare le release: <https://github.com/apache/superset/releases?q=superset-helm-chart>
2. Leggere `UPGRADING.md` del chart upstream per i breaking change sui values.
3. Bump di `dependencies[0].version` in `Chart.yaml`, poi `helm dependency update ./helm`.
4. Bump di `version` (e, se cambia l'immagine, di `appVersion`) in `Chart.yaml`.
5. `helm template` per verificare il diff prima di rilasciare.

## TODO prima del primo deploy reale

- [ ] confermare hostname, `ingressClassName` e gestione TLS con il team infra
- [ ] sostituire gli endpoint placeholder di PostgreSQL e Redis in `values-dev.yaml`
- [ ] sostituire gli URL placeholder `AUTH_BASE_URL` / `DEBT_POSITIONS_BASE_URL`
- [ ] creare il secret esterno via ESO / Key Vault CSI
- [ ] verificare se serve un `imagePullSecrets` o se l'ACR e' collegato all'AKS
- [ ] aggiungere lo stage di deploy in `.devops/deploy-pipelines.yml`
- [ ] valutare `supersetCeleryBeat.enabled: true` se servono alert & report
