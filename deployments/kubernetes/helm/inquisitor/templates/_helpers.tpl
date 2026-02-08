{{/* Generate chart name */}}
{{- define "inquisitor.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/* Generate full name */}}
{{- define "inquisitor.fullname" -}}
{{- if .Values.global.name -}}
{{- .Values.global.name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{/* Generate common labels */}}
{{- define "inquisitor.labels" -}}
helm.sh/chart: {{ include "inquisitor.chart" . }}
{{ include "inquisitor.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/* Generate selector labels */}}
{{- define "inquisitor.selectorLabels" -}}
app.kubernetes.io/name: {{ include "inquisitor.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/* Generate service account name */}}
{{- define "inquisitor.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "inquisitor.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/* Generate environment name */}}
{{- define "inquisitor.environment" -}}
{{- .Values.global.environment | default "production" -}}
{{- end -}}

{{/* Generate image pull secret */}}
{{- define "inquisitor.imagePullSecrets" -}}
{{- if .Values.image.imagePullSecrets -}}
imagePullSecrets:
{{ toYaml .Values.image.imagePullSecrets | indent 2 }}
{{- end -}}
{{- end -}}

{{/* Generate database URL */}}
{{- define "inquisitor.databaseUrl" -}}
{{- if .Values.artifactRegistry.database.enabled -}}
{{- $host := .Values.artifactRegistry.database.host -}}
{{- $port := .Values.artifactRegistry.database.port -}}
{{- $database := .Values.artifactRegistry.database.database -}}
{{- $username := .Values.artifactRegistry.database.username -}}
{{- $sslMode := .Values.artifactRegistry.database.sslMode -}}
postgresql://{{ $username }}:$(DATABASE_PASSWORD)@{{ $host }}:{{ $port }}/{{ $database }}?sslmode={{ $sslMode }}
{{- else -}}
sqlite:///data/inquisitor.db
{{- end -}}
{{- end -}}

{{/* Generate Redis URL */}}
{{- define "inquisitor.redisUrl" -}}
{{- if .Values.cache.enabled -}}
{{- $host := .Values.cache.redis.host -}}
{{- $port := .Values.cache.redis.port -}}
{{- $database := .Values.cache.redis.database -}}
redis://:$(REDIS_PASSWORD)@{{ $host }}:{{ $port }}/{{ $database }}
{{- else -}}
memory://
{{- end -}}
{{- end -}}

{{/* Generate S3 endpoint */}}
{{- define "inquisitor.s3Endpoint" -}}
{{- if eq .Values.artifactRegistry.storageBackend "s3" -}}
https://{{ .Values.artifactRegistry.s3.bucket }}.s3.{{ .Values.artifactRegistry.s3.region }}.amazonaws.com
{{- end -}}
{{- end -}}
