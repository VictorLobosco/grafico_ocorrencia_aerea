CREATE SCHEMA IF NOT EXISTS ocorrencia;

CREATE TABLE IF NOT EXISTS ocorrencia.ocorrencia
(
    codigo_ocorrencia bigint,
    codigo_ocorrencia1 bigint,
    codigo_ocorrencia2 bigint,
    codigo_ocorrencia3 bigint,
    codigo_ocorrencia4 bigint,
    ocorrencia_classificacao text,
    ocorrencia_latitude text,
    ocorrencia_longitude text,
    ocorrencia_cidade text,
    ocorrencia_uf text,
    ocorrencia_pais text,
    ocorrencia_aerodromo text,
    ocorrencia_dia timestamp without time zone,
    ocorrencia_hora text,
    investigacao_aeronave_liberada text,
    investigacao_status text,
    divulgacao_relatorio_numero text,
    divulgacao_relatorio_publicado text,
    divulgacao_dia_publicacao text,
    total_recomendacoes bigint,
    total_aeronaves_envolvidas bigint,
    ocorrencia_saida_pista text,
    ocorrencia_mes text
);

CREATE TABLE IF NOT EXISTS ocorrencia.ocorrencia_tipo
(
    codigo_ocorrencia1 bigint,
    ocorrencia_tipo text,
    ocorrencia_tipo_categoria text,
    taxonomia_tipo_icao text
);

CREATE TABLE IF NOT EXISTS ocorrencia.aeronave
(
    codigo_ocorrencia2 bigint,
    aeronave_matricula text,
    aeronave_operador_categoria text,
    aeronave_tipo_veiculo text,
    aeronave_fabricante text,
    aeronave_modelo text,
    aeronave_tipo_icao text,
    aeronave_motor_tipo text,
    aeronave_motor_quantidade text,
    aeronave_pmd bigint,
    aeronave_pmd_categoria bigint,
    aeronave_assentos text,
    aeronave_ano_fabricacao text,
    aeronave_pais_fabricante text,
    aeronave_pais_registro text,
    aeronave_registro_categoria text,
    aeronave_registro_segmento text,
    aeronave_voo_origem text,
    aeronave_voo_destino text,
    aeronave_fase_operacao text,
    aeronave_tipo_operacao text,
    aeronave_nivel_dano text,
    aeronave_fatalidades_total bigint
);

CREATE TABLE IF NOT EXISTS ocorrencia.fator_contribuinte
(
    codigo_ocorrencia3 bigint,
    fator_nome text,
    fator_aspecto text,
    fator_condicionante text,
    fator_area text
);

CREATE TABLE IF NOT EXISTS ocorrencia.recomendacao
(
    codigo_ocorrencia4 bigint,
    recomendacao_numero text,
    recomendacao_dia_assinatura text,
    recomendacao_dia_encaminhamento text,
    recomendacao_dia_feedback text,
    recomendacao_conteudo text,
    recomendacao_status text,
    recomendacao_destinatario_sigla text,
    recomendacao_destinatario text
);

CREATE TABLE IF NOT EXISTS public.db_info (
  last_hash VARCHAR PRIMARY KEY,
  last_date VARCHAR
);