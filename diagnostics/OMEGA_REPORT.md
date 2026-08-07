══════════════════════════════════════════════════════════════════════
ℹ️  OMEGA REPORT — RENDERIZADOR PURO
  Versión Omega: 12.2-puro
  Omega no crea datos. Solo imprime el paquete entregado por Engine.
══════════════════════════════════════════════════════════════════════

══════════════════════════════════════════════════════════════════════
  ▶️  INFORMACIÓN DEL RUN
══════════════════════════════════════════════════════════════════════
  version_engine: 18.3
  estado_engine: OPERATIVO
  esquema_contrato: VPSI-CONTRACT-1.0
  total_modulos: 8
  timestamp: 2026-08-07T05:05:29.127763+00:00

══════════════════════════════════════════════════════════════════════
  INFORMACIÓN DEL RUN
══════════════════════════════════════════════════════════════════════
  version_engine: 18.3
  esquema_contrato: VPSI-CONTRACT-1.0
  version_contrato_requerida: 1.0
  api_engine: 1.0
  estado_engine: OPERATIVO
  invocador_id: omega_report
  total_modulos: 8
  errores_arranque:
    []
  advertencias:
    []
  trazas_n: 24
  timestamp: 2026-08-07T05:05:29.127728+00:00

══════════════════════════════════════════════════════════════════════
  MÓDULO AX/axiomas
══════════════════════════════════════════════════════════════════════
  id: AX
  nombre: axiomas
  rol: AX
  version: 9.6
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 9.5
  api_engine: >=1.0
  descripcion: Responsable del conocimiento axiomático del sistema. Mantiene, valida, organiza y expone todas las declaraciones oficiales del repositorio.
  funcion: Ser la fuente oficial del conocimiento axiomático: cargar, normalizar, validar coherencia, responder consultas, citar declaraciones y exponer generatividad.
  no_hace:
    • No calcula Tru_total ni Tru_Ri
    • No clasifica entrada de usuario (eso es CX)
    • No orquesta el sistema (eso es Engine)
    • No genera reportes de otros módulos
    • No modifica declaraciones ajenas
  autoridad:
    • Exponer cualquier axioma, lema, teorema, corolario o definición
    • Responder consultas por id, dominio, sujeto, relación, objeto
    • Citar y relacionar declaraciones del grafo
    • Verificar coherencia interna
    • Reportar estado, salud, inventario y diagnóstico propios
    • Notificar a DiagnosticoGlobal cuando hay choques o errores
  conocimiento_exportable:
    • declaraciones
    • referencias
    • dependencias
    • dominios
    • generatividad
    • choques
    • inventario
    • estado
    • reporte
    • diagnostico
  consultas_soportadas:
    • buscar_por_id
    • buscar_por_dominio
    • obtener_generatividad
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • verificar_coherencia
    • ids_dominio_k_o
    • recolectar
  requiere:
    []
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    modificar: False
    alterar: False
    reescribir: False
  capacidades:
    • verificar
    • barrer
    • verificar_salida
    • inventario
    • axiomas
    • declaraciones
    • generatividad
    • por_dominio
    • ids_dominio_k_o
    • recolectar
    • reporte
    • diagnostico
    • buscar_por_id
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia interna del módulo.
      entrada: declaraciones_externas opcional (dict)
      salida: dict con coherente, choques, errores, declaraciones, cuerpos, por_tipo
    barrer:
      descripcion: Analiza coherencia de todas las declaraciones (contradicción directa y de cota).
      entrada: declaraciones_externas opcional (dict)
      salida: dict con coherente, choques, errores, declaraciones, cuerpos, por_tipo, ids_dominio_k_o
    verificar_salida:
      descripcion: Comprueba si una salida de barrer/verificar es coherente.
      entrada: salida: dict
      salida: bool
    inventario:
      descripcion: Inventario completo del módulo (declaraciones, cuerpos, capacidades).
      entrada: peticion opcional
      salida: dict con id, nombre, rol, version, declaraciones, cuerpos, capacidades
    axiomas:
      descripcion: Devuelve las declaraciones si el módulo es coherente; lista vacía si no.
      entrada: declaraciones_externas opcional (dict)
      salida: list[dict] de declaraciones normalizadas
    declaraciones:
      descripcion: Igual que axiomas: declaraciones normalizadas si coherente.
      entrada: declaraciones_externas opcional (dict)
      salida: list[dict] de declaraciones normalizadas
    generatividad:
      descripcion: Mide generatividad operativa y canónica (TR1).
      entrada: ninguna
      salida: dict con theta_n, pares, im_vs_theta, capa canonica, dominios, u1_proxy
    por_dominio:
      descripcion: Filtra declaraciones por dominio en gobierna.
      entrada: dominio: str; declaraciones_externas opcional
      salida: list[dict] de declaraciones del dominio
    ids_dominio_k_o:
      descripcion: Ids de declaraciones ligadas a dominios K/O o Def-5.3.1.
      entrada: declaraciones_externas opcional (dict)
      salida: list[str] de ids ordenados
    recolectar:
      descripcion: Carga y normaliza todas las declaraciones de los cuerpos del módulo.
      entrada: declaraciones_externas opcional (dict)
      salida: tuple[list[dict], list[dict]] → (declaraciones, errores)
    reporte:
      descripcion: Reporte interno de estado del módulo.
      entrada: ninguna
      salida: dict con estado, coherente, declaraciones, choques, errores, capacidades
    diagnostico:
      descripcion: Diagnóstico: qué me sucede, qué falta, qué está mal, qué necesito.
      entrada: ninguna
      salida: dict con estado, problemas, advertencias, recomendaciones
    buscar_por_id:
      descripcion: Busca y cita una declaración por su id.
      entrada: id_decl: str
      salida: dict de la declaración o None
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • las capacidades declaradas son siempre callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
    • este módulo siempre puede reportar su propio estado
  reporte:
    id: AX
    modulo: axiomas
    rol: AX
    version: 9.6
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    declaraciones: 190
    choques: 0
    errores: 0
    cuerpos:
      • Anclas_de_Medicion_AM_AX
      • VPSI_AX
      • contexto_AX
    por_tipo:
      axioma: 74
      lema: 19
      teorema: 51
      corolario: 40
      definicion: 6
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • inventario
      • axiomas
      • declaraciones
      • generatividad
      • por_dominio
      • ids_dominio_k_o
      • recolectar
      • reporte
      • diagnostico
      • buscar_por_id
    requiere:
      []
    autoridad:
      • Exponer cualquier axioma, lema, teorema, corolario o definición
      • Responder consultas por id, dominio, sujeto, relación, objeto
      • Citar y relacionar declaraciones del grafo
      • Verificar coherencia interna
      • Reportar estado, salud, inventario y diagnóstico propios
      • Notificar a DiagnosticoGlobal cuando hay choques o errores
    conocimiento_exportable:
      • declaraciones
      • referencias
      • dependencias
      • dominios
      • generatividad
      • choques
      • inventario
      • estado
      • reporte
      • diagnostico
    consultas_soportadas:
      • buscar_por_id
      • buscar_por_dominio
      • obtener_generatividad
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • verificar_coherencia
      • ids_dominio_k_o
      • recolectar
  diagnostico:
    id: AX
    modulo: axiomas
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    coherente: True
    declaraciones: 190
    choques_n: 0
    errores_n: 0
  inventario:
    id: AX
    nombre: axiomas
    rol: AX
    version: 9.6
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    tipos:
      • axioma
      • lema
      • teorema
      • corolario
      • definicion
    declaraciones: 190
    por_tipo:
      axioma: 74
      lema: 19
      teorema: 51
      corolario: 40
      definicion: 6
    cuerpos:
      • Anclas_de_Medicion_AM_AX
      • VPSI_AX
      • contexto_AX
    errores:
      []
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • inventario
      • axiomas
      • declaraciones
      • generatividad
      • por_dominio
      • ids_dominio_k_o
      • recolectar
      • reporte
      • diagnostico
      • buscar_por_id
    requiere:
      []
    autoridad:
      • Exponer cualquier axioma, lema, teorema, corolario o definición
      • Responder consultas por id, dominio, sujeto, relación, objeto
      • Citar y relacionar declaraciones del grafo
      • Verificar coherencia interna
      • Reportar estado, salud, inventario y diagnóstico propios
      • Notificar a DiagnosticoGlobal cuando hay choques o errores
    conocimiento_exportable:
      • declaraciones
      • referencias
      • dependencias
      • dominios
      • generatividad
      • choques
      • inventario
      • estado
      • reporte
      • diagnostico
    consultas_soportadas:
      • buscar_por_id
      • buscar_por_dominio
      • obtener_generatividad
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • verificar_coherencia
      • ids_dominio_k_o
      • recolectar
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
      • este módulo siempre puede reportar su propio estado
    vigila:
      • contradiccion_directa
      • contradiccion_de_cota
    ids_dominio_k_o:
      • A1
      • A10
      • A11
      • A2
      • A3
      • A4
      • A5
      • A6
      • A7
      • A8
      • A9
      • AM-A3
      • AM-C3
      • AM-D1
      • AM-D3
      • AM-D4
      • AM-D6
      • AM-L3
      • AM-T1
      • B-Canonical
      • CX-A1
      • CX-A10
      • CX-A11
      • CX-A12
      • CX-A13
      • CX-A14
      • CX-A15
      • CX-A16
      • CX-A17
      • CX-A18
      • CX-A19
      • CX-A2
      • CX-A20
      • CX-A21
      • CX-A22
      • CX-A23
      • CX-A24
      • CX-A25
      • CX-A26
      • CX-A27
      • CX-A3
      • CX-A4
      • CX-A5
      • CX-A6
      • CX-A7
      • CX-A8
      • CX-A9
      • CX-C1
      • CX-C10
      • CX-C11
      • CX-C12
      • CX-C13
      • CX-C14
      • CX-C15
      • CX-C16
      • CX-C17
      • CX-C18
      • CX-C2
      • CX-C3
      • CX-C4
      • CX-C5
      • CX-C6
      • CX-C7
      • CX-C8
      • CX-C9
      • CX-D16
      • CX-D17
      • CX-D18
      • CX-D19
      • CX-D20
      • CX-D21
      • CX-L1
      • CX-L10
      • CX-L11
      • CX-L2
      • CX-L3
      • CX-L4
      • CX-L5
      • CX-L6
      • CX-L7
      • CX-L8
      • CX-L9
      • CX-T1
      • CX-T10
      • CX-T11
      • CX-T12
      • CX-T13
      • CX-T14
      • CX-T15
      • CX-T16
      • CX-T17
      • CX-T2
      • CX-T3
      • CX-T4
      • CX-T5
      • CX-T6
      • CX-T7
      • CX-T8
      • CX-T9
      • Def-5.3.1
      • E1
      • E2
      • E3
      • I
      • IV
      • M.1
      • T1
      • T10
      • T11
      • T13
      • T14
      • T15
      • T4
      • T5
      • T6
      • T7
      • TA3
      • TA4
      • TT.11.5
      • TT.13.1
      • TT.6.1
      • TT.7.4
      • VIII
      • X
      • beta-Godel
      • beta-Private-1
      • beta-Private-2
      • beta-Private-3
      • beta-Private-4
    nota: Def-5.3.1 y dominio O viven en los cuerpos cargados; este módulo los vigila y expone, no los clasifica en entrada.

══════════════════════════════════════════════════════════════════════
  MÓDULO CH/cache
══════════════════════════════════════════════════════════════════════
  id: CH
  nombre: cache
  rol: CH
  version: 4.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Registrador universal de eventos. Libro de actas del sistema. Conserva evidencia objetiva. Categorías dinámicas. No interpreta. No deduce. No reconstruye. No calcula.
  funcion: Registrar exactamente lo que ocurrió durante la ejecución y exponer lecturas filtradas por campos del registro. Nada más.
  no_hace:
    • No interpreta
    • No deduce ni infiere
    • No reconstruye ciclos
    • No genera grafos ni árboles
    • No explica razonamientos ni causas
    • No calcula C / L / K / Tru
    • No descubre relaciones
    • No altera evidencia depositada
    • No inicia operaciones
    • No envía reportes a otros módulos
  autoridad:
    • Registrar eventos depositados por Engine o Centinela
    • Entregar lecturas filtradas por campos del registro
    • Exponer categorías descubiertas dinámicamente
    • Verificar integridad del registro (forma, no contenido)
    • Reportar estado, inventario y diagnóstico propios
  conocimiento_exportable:
    • depositar
    • leer
    • leer_eventos
    • leer_por_ciclo
    • leer_por_modulo
    • leer_por_tipo
    • leer_por_categoria
    • leer_por_capacidad
    • leer_por_origen
    • leer_por_destino
    • leer_por_estado
    • leer_por_seq
    • leer_por_timestamp
    • categorias
    • inventario
    • reporte
    • diagnostico
    • backend_para_centinela
  consultas_soportadas:
    • depositar_evento
    • leer_eventos
    • filtrar_por_campo
    • listar_categorias
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • verificar_integridad_registro
  requiere:
    []
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    modificar: False
    alterar: False
    reescribir: False
  capacidades:
    • verificar
    • barrer
    • depositar
    • leer
    • leer_eventos
    • leer_por_ciclo
    • leer_por_modulo
    • leer_por_tipo
    • leer_por_categoria
    • leer_por_capacidad
    • leer_por_origen
    • leer_por_destino
    • leer_por_estado
    • leer_por_seq
    • leer_por_timestamp
    • categorias
    • inventario
    • reporte
    • diagnostico
    • verificar_salida
    • backend_para_centinela
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Integridad formal del registro.
      entrada: ninguna
      salida: dict con coherente, inmutable, errores, resumen
    barrer:
      descripcion: Verifica forma del registro: seq creciente, timestamps, payload dict. No interpreta contenido.
      entrada: ninguna
      salida: dict con coherente, inmutable, errores, resumen
    depositar:
      descripcion: Registra un evento neutro. Única vía de escritura. Append-only. Categorías se descubren al depositar.
      entrada: tipo, payload, ciclo_id?, run_id?, origen?, destino?, modulo?, capacidad?, categoria?, estado?
      salida: dict del evento registrado
    leer:
      descripcion: Lectura genérica con filtros opcionales por campo.
      entrada: filtros opcionales por campo del registro
      salida: list[dict]
    leer_eventos:
      descripcion: Alias de leer sin filtros (todos los eventos).
      entrada: ninguna
      salida: list[dict]
    leer_por_ciclo:
      descripcion: Eventos de un ciclo_id.
      entrada: ciclo_id: str
      salida: list[dict]
    leer_por_modulo:
      descripcion: Eventos de un módulo.
      entrada: modulo: str, ciclo_id?
      salida: list[dict]
    leer_por_tipo:
      descripcion: Eventos de un tipo.
      entrada: tipo: str, ciclo_id?
      salida: list[dict]
    leer_por_categoria:
      descripcion: Eventos de una categoría (dinámica).
      entrada: categoria: str, ciclo_id?
      salida: list[dict]
    leer_por_capacidad:
      descripcion: Eventos de una capacidad.
      entrada: capacidad: str, ciclo_id?
      salida: list[dict]
    leer_por_origen:
      descripcion: Eventos con un origen dado.
      entrada: origen: str, ciclo_id?
      salida: list[dict]
    leer_por_destino:
      descripcion: Eventos con un destino dado.
      entrada: destino: str, ciclo_id?
      salida: list[dict]
    leer_por_estado:
      descripcion: Eventos con un estado dado.
      entrada: estado: str, ciclo_id?
      salida: list[dict]
    leer_por_seq:
      descripcion: Eventos en un rango de seq.
      entrada: desde_seq?, hasta_seq?
      salida: list[dict]
    leer_por_timestamp:
      descripcion: Eventos en un rango de timestamp.
      entrada: desde_timestamp?, hasta_timestamp?
      salida: list[dict]
    categorias:
      descripcion: Categorías descubiertas dinámicamente hasta ahora.
      entrada: ninguna
      salida: list[str]
    inventario:
      descripcion: Inventario del módulo y resumen del registro.
      entrada: ninguna
      salida: dict con id, version, memoria, categorias, capacidades
    reporte:
      descripcion: Reporte interno de estado del módulo CH.
      entrada: ninguna
      salida: dict con estado, coherente, memoria, capacidades
    diagnostico:
      descripcion: Diagnóstico de integridad formal del registro.
      entrada: ninguna
      salida: dict con estado, problemas, advertencias, recomendaciones
    verificar_salida:
      descripcion: Comprueba forma de una salida de barrer o depósito.
      entrada: salida: dict
      salida: bool
    backend_para_centinela:
      descripcion: Adaptador estable CacheBackend para Centinela. Centinela no conoce la implementación interna.
      entrada: ninguna
      salida: CacheBackend
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • las capacidades declaradas son siempre callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • este módulo no calcula
    • este módulo no interpreta
    • este módulo no deduce ni infiere
    • este módulo no reconstruye ni genera grafos
    • la evidencia depositada nunca se modifica
    • la evidencia depositada nunca se sobrescribe
    • la evidencia depositada nunca se reordena
    • la evidencia depositada nunca desaparece durante el ciclo
    • toda información nueva se incorpora solo como evento nuevo
    • las categorías son dinámicas; no hay lista fija de dominios
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
  reporte:
    id: CH
    modulo: cache
    rol: CH
    version: 4.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    inmutable: True
    errores:
      []
    memoria:
      total_eventos: 0
      ciclos: 0
      seq_actual: 0
      por_tipo:
      por_categoria:
      categorias:
        []
      inmutable: True
    categorias:
      []
    capacidades:
      • verificar
      • barrer
      • depositar
      • leer
      • leer_eventos
      • leer_por_ciclo
      • leer_por_modulo
      • leer_por_tipo
      • leer_por_categoria
      • leer_por_capacidad
      • leer_por_origen
      • leer_por_destino
      • leer_por_estado
      • leer_por_seq
      • leer_por_timestamp
      • categorias
      • inventario
      • reporte
      • diagnostico
      • verificar_salida
      • backend_para_centinela
    requiere:
      []
    autoridad:
      • Registrar eventos depositados por Engine o Centinela
      • Entregar lecturas filtradas por campos del registro
      • Exponer categorías descubiertas dinámicamente
      • Verificar integridad del registro (forma, no contenido)
      • Reportar estado, inventario y diagnóstico propios
    conocimiento_exportable:
      • depositar
      • leer
      • leer_eventos
      • leer_por_ciclo
      • leer_por_modulo
      • leer_por_tipo
      • leer_por_categoria
      • leer_por_capacidad
      • leer_por_origen
      • leer_por_destino
      • leer_por_estado
      • leer_por_seq
      • leer_por_timestamp
      • categorias
      • inventario
      • reporte
      • diagnostico
      • backend_para_centinela
    consultas_soportadas:
      • depositar_evento
      • leer_eventos
      • filtrar_por_campo
      • listar_categorias
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • verificar_integridad_registro
  diagnostico:
    id: CH
    modulo: cache
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      • Registro vacío (legítimo al inicio del ciclo)
    recomendaciones:
      []
    coherente: True
    inmutable: True
    total_eventos: 0
    ciclos: 0
    seq_actual: 0
    categorias_n: 0
  inventario:
    id: CH
    nombre: cache
    rol: CH
    version: 4.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    funcion: Registrador universal de eventos. Libro de actas. Append-only. No interpreta.
    memoria:
      total_eventos: 0
      ciclos: 0
      seq_actual: 0
      por_tipo:
      por_categoria:
      categorias:
        []
      inmutable: True
    categorias:
      []
    campos_registro:
      • seq
      • timestamp
      • run_id
      • ciclo_id
      • origen
      • destino
      • modulo
      • capacidad
      • tipo
      • categoria
      • estado
      • payload
    capacidades:
      • verificar
      • barrer
      • depositar
      • leer
      • leer_eventos
      • leer_por_ciclo
      • leer_por_modulo
      • leer_por_tipo
      • leer_por_categoria
      • leer_por_capacidad
      • leer_por_origen
      • leer_por_destino
      • leer_por_estado
      • leer_por_seq
      • leer_por_timestamp
      • categorias
      • inventario
      • reporte
      • diagnostico
      • verificar_salida
      • backend_para_centinela
    requiere:
      []
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no calcula
      • este módulo no interpreta
      • este módulo no deduce ni infiere
      • este módulo no reconstruye ni genera grafos
      • la evidencia depositada nunca se modifica
      • la evidencia depositada nunca se sobrescribe
      • la evidencia depositada nunca se reordena
      • la evidencia depositada nunca desaparece durante el ciclo
      • toda información nueva se incorpora solo como evento nuevo
      • las categorías son dinámicas; no hay lista fija de dominios
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
    nota: CACHE no sabe lo que ocurrió. Solo sabe qué fue registrado. Análisis de trazabilidad: módulo futuro, no este.

══════════════════════════════════════════════════════════════════════
  MÓDULO CA/calculator
══════════════════════════════════════════════════════════════════════
  id: CA
  nombre: calculator
  rol: CA
  version: 2.3
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.2
  api_engine: >=1.0
  descripcion: Unica autoridad del dominio de calculo estructural. Calcula C, L, K. Cada factor se reporta como un solo objeto con fraccion y decimal (ej: 7/9 = 0.778). No calcula Tru (FO).
  funcion: Pipeline: evidencia -> C/L/K -> centinela -> ID compuesto -> historial liviano. Valor oficial = Fraction. Decimal via Decimal.
  no_hace:
    • No calcula Tru_Ri ni Tru_total
    • No redefine constantes, axiomas ni formulas
    • No orquesta el sistema
    • No estima por intuicion
    • No duplica campos de factor en la raiz de la salida
  autoridad:
    • Unica autoridad para calcular C, L, K
    • Reportar cada factor como fraccion = decimal en un solo objeto
    • Validar evidencia y explicar calculos con trazabilidad real
    • Auditar integridad del dominio
  conocimiento_exportable:
    • C
    • L
    • K
    • factores
    • UNDEFINED
    • evidencia
    • versiones_utilizadas
    • contratos_utilizados
    • historial
    • explicaciones
    • inventario
    • estado
    • reporte
    • diagnostico
  consultas_soportadas:
    • calcular
    • calcular_C
    • calcular_L
    • calcular_K
    • calcular_factor
    • representar
    • validar_evidencia
    • explicar_calculo
    • verificar_coherencia
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • leer_ids_escala
    • historial
  requiere:
    []
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    modificar: False
    alterar: False
    reescribir: False
  capacidades:
    • calcular
    • calcular_C
    • calcular_L
    • calcular_K
    • calcular_factor
    • representar
    • validar_evidencia
    • explicar_calculo
    • verificar
    • barrer
    • inventario
    • reporte
    • diagnostico
    • leer_ids_escala
    • verificar_salida
    • historial
  capacidades_meta:
    calcular:
      descripcion: Pipeline completo. C/L/K son objetos unicos con fraccion+decimal (ej display: 7/9 = 0.778).
      entrada: peticion: dict
      salida: dict con id_calculo, C, L, K, evidencia, versiones_utilizadas, centinela, errores
    calcular_C:
      descripcion: Factor C como objeto fraccion+decimal.
      entrada: peticion: dict
      salida: dict con C, ruta, notas, evidencia
    calcular_L:
      descripcion: Factor L como objeto (o UNDEFINED).
      entrada: peticion: dict
      salida: dict con L, p, r, ruta, notas, evidencia
    calcular_K:
      descripcion: Factor K como objeto (o None sin O).
      entrada: peticion: dict
      salida: dict con K, ruta, notas, evidencia
    calcular_factor:
      descripcion: Factor por nombre C|L|K.
      entrada: factor: str, peticion: dict
      salida: dict del factor
    representar:
      descripcion: Fraction -> objeto con fraccion, numerador, denominador, decimal, display (7/9 = 0.778). Sin float.
      entrada: valor: Fraction|UNDEFINED|None, precision: int=3
      salida: dict valor completo
    validar_evidencia:
      descripcion: Valida lista de evidencia sin calcular: estructura, rechazados, conflicto de versiones del mismo modulo.
      entrada: evidencia: list[dict]
      salida: dict con ok, problemas, advertencias, evidencia_normalizada
    explicar_calculo:
      descripcion: Explica un calculo por id usando evidencia real almacenada.
      entrada: id_calculo: str
      salida: dict explicativo dinamico o None
    verificar:
      descripcion: Centinela de integridad (APIs, hashes, choques).
      entrada: ninguna
      salida: dict con coherente, errores, choques, hashes
    barrer:
      descripcion: Alias de verificar.
      entrada: ninguna
      salida: dict con coherente, errores, choques, hashes
    inventario:
      descripcion: Inventario del dominio de calculo.
      entrada: peticion opcional
      salida: dict con capacidades, factores, archivos, hashes
    reporte:
      descripcion: Reporte de estado de CA.
      entrada: ninguna
      salida: dict con estado, coherente, factores_api
    diagnostico:
      descripcion: Diagnostico de problemas y recomendaciones.
      entrada: ninguna
      salida: dict con estado, problemas, advertencias, recomendaciones
    leer_ids_escala:
      descripcion: Ids de escala reconocidos.
      entrada: ninguna
      salida: dict con ids, n, origenes
    verificar_salida:
      descripcion: Forma minima: C, L, K, id_calculo; cada factor con display.
      entrada: salida: dict
      salida: bool
    historial:
      descripcion: Buffer liviano de ultimos calculos.
      entrada: limite opcional: int
      salida: list[dict]
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • CA es la unica autoridad del dominio de calculo estructural
    • todo calculo interno utiliza Fraction como valor oficial
    • toda salida de factor es un solo objeto con fraccion+decimal (ej: 7/9 = 0.778)
    • no se duplican campos de factor en la raiz de la respuesta
    • float nunca es la fuente del decimal; se usa Decimal
    • ningun calculo sale sin centinela ni ID unico compuesto
    • toda magnitud registra evidencia trazable con id_evidencia
    • K ausente sin contexto/O es legitimo (Def-5.3.1)
    • L = UNDEFINED cuando p=0 (AM-D6 / AM-A3)
  reporte:
    id: CA
    modulo: calculator
    rol: CA
    version: 2.3
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    factores_api:
      • C
      • K
      • L
    archivos:
      • coherencia.py
      • conteos.py
      • correlacion_k.py
      • escalas_ids.py
      • logica.py
    hashes:
      __init__.py:
        archivo: __init__.py
        sha256: a310236c3ceacc83a43c6f96924394eaa8651b1aa5c2f978e951b7fe2de341fe
        tamano: 51021
        timestamp_mtime: 2026-08-07T05:05:24.927508+00:00
      coherencia.py:
        archivo: coherencia.py
        sha256: ba9d374bca15dc4b36766d151068fdf9895166a60a4352aa0b2706f1a3714313
        tamano: 6153
        timestamp_mtime: 2026-08-07T05:05:24.927991+00:00
      conteos.py:
        archivo: conteos.py
        sha256: 19c30b65365863ef671d9e03aba20e9096b97033681120c4c9ca49dadf352330
        tamano: 20987
        timestamp_mtime: 2026-08-07T05:05:24.927991+00:00
      correlacion_k.py:
        archivo: correlacion_k.py
        sha256: b1cc60d3cc07db792ad4978ff6b14f810d406a62aeae6f552b1795d6695200ab
        tamano: 5546
        timestamp_mtime: 2026-08-07T05:05:24.927991+00:00
      escalas_ids.py:
        archivo: escalas_ids.py
        sha256: 1db219e396c1a9c1cbfdf29ff92842b2b151907c07c6043a70c46349661ba128
        tamano: 2895
        timestamp_mtime: 2026-08-07T05:05:24.927991+00:00
      logica.py:
        archivo: logica.py
        sha256: 39b805c383a02e670d4fd1158e0c95b8e2e41c2d451c8ca377f497c802c236f1
        tamano: 4803
        timestamp_mtime: 2026-08-07T05:05:24.927991+00:00
    historial_n: 0
    errores_n: 0
    choques_n: 0
    capacidades:
      • calcular
      • calcular_C
      • calcular_L
      • calcular_K
      • calcular_factor
      • representar
      • validar_evidencia
      • explicar_calculo
      • verificar
      • barrer
      • inventario
      • reporte
      • diagnostico
      • leer_ids_escala
      • verificar_salida
      • historial
    regla_salida: un objeto por factor: fraccion = decimal (7/9 = 0.778)
    autoridad:
      • Unica autoridad para calcular C, L, K
      • Reportar cada factor como fraccion = decimal en un solo objeto
      • Validar evidencia y explicar calculos con trazabilidad real
      • Auditar integridad del dominio
    conocimiento_exportable:
      • C
      • L
      • K
      • factores
      • UNDEFINED
      • evidencia
      • versiones_utilizadas
      • contratos_utilizados
      • historial
      • explicaciones
      • inventario
      • estado
      • reporte
      • diagnostico
  diagnostico:
    id: CA
    modulo: calculator
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    coherente: True
    factores_api:
      • C
      • K
      • L
    historial_n: 0
  inventario:
    id: CA
    nombre: calculator
    rol: CA
    version: 2.3
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    archivos:
      • coherencia.py
      • conteos.py
      • correlacion_k.py
      • escalas_ids.py
      • logica.py
    hashes:
      __init__.py:
        archivo: __init__.py
        sha256: a310236c3ceacc83a43c6f96924394eaa8651b1aa5c2f978e951b7fe2de341fe
        tamano: 51021
        timestamp_mtime: 2026-08-07T05:05:24.927508+00:00
      coherencia.py:
        archivo: coherencia.py
        sha256: ba9d374bca15dc4b36766d151068fdf9895166a60a4352aa0b2706f1a3714313
        tamano: 6153
        timestamp_mtime: 2026-08-07T05:05:24.927991+00:00
      conteos.py:
        archivo: conteos.py
        sha256: 19c30b65365863ef671d9e03aba20e9096b97033681120c4c9ca49dadf352330
        tamano: 20987
        timestamp_mtime: 2026-08-07T05:05:24.927991+00:00
      correlacion_k.py:
        archivo: correlacion_k.py
        sha256: b1cc60d3cc07db792ad4978ff6b14f810d406a62aeae6f552b1795d6695200ab
        tamano: 5546
        timestamp_mtime: 2026-08-07T05:05:24.927991+00:00
      escalas_ids.py:
        archivo: escalas_ids.py
        sha256: 1db219e396c1a9c1cbfdf29ff92842b2b151907c07c6043a70c46349661ba128
        tamano: 2895
        timestamp_mtime: 2026-08-07T05:05:24.927991+00:00
      logica.py:
        archivo: logica.py
        sha256: 39b805c383a02e670d4fd1158e0c95b8e2e41c2d451c8ca377f497c802c236f1
        tamano: 4803
        timestamp_mtime: 2026-08-07T05:05:24.927991+00:00
    factores_api:
      • C
      • K
      • L
    conteos_disponible: True
    escalas_ids_disponible: True
    ids_escala:
      ids:
        • tru_atomo
        • tru_frase
        • tru_sujeto
        • tru_conversacion
        • tru_repositorio
      n: 5
      origenes:
        • escalas_ids
      disponible: True
    coherente: True
    historial_n: 0
    capacidades:
      • calcular
      • calcular_C
      • calcular_L
      • calcular_K
      • calcular_factor
      • representar
      • validar_evidencia
      • explicar_calculo
      • verificar
      • barrer
      • inventario
      • reporte
      • diagnostico
      • leer_ids_escala
      • verificar_salida
      • historial
    requiere:
      []
    invariantes:
      • CA es la unica autoridad del dominio de calculo estructural
      • todo calculo interno utiliza Fraction como valor oficial
      • toda salida de factor es un solo objeto con fraccion+decimal (ej: 7/9 = 0.778)
      • no se duplican campos de factor en la raiz de la respuesta
      • float nunca es la fuente del decimal; se usa Decimal
      • ningun calculo sale sin centinela ni ID unico compuesto
      • toda magnitud registra evidencia trazable con id_evidencia
      • K ausente sin contexto/O es legitimo (Def-5.3.1)
      • L = UNDEFINED cuando p=0 (AM-D6 / AM-A3)
    precision_decimal_default: 3
    regla_salida: un objeto por factor: fraccion = decimal (7/9 = 0.778)

══════════════════════════════════════════════════════════════════════
  MÓDULO CC/catalogo_citaciones
══════════════════════════════════════════════════════════════════════
  id: CC
  nombre: catalogo_citaciones
  rol: CC
  version: 2.1
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Glosario de IDs del repositorio. Rol CC. Lee y organiza categorias/*.py. Los IDs viven ahí, no en el INIT. Engine consulta IDs para citar o reportar. No calcula. No interpreta pedidos. No envía reportes a terceros.
  funcion: Exponer el catálogo de IDs del repositorio, responder por_id / ids / esquema y reportar coherencia propia.
  no_hace:
    • No calcula Tru_Ri / Tru_total / C / L / K
    • No aplica α / β
    • No hace conteos
    • No clasifica O
    • No orquesta el ciclo
    • No envía reportes a otros módulos
    • No sustituye CIT / CA / FO / AX / CX / MC / RE / TX / CH
    • No interpreta pedidos
  autoridad:
    • Declarar los IDs disponibles en el catálogo
    • Resolver consulta por_id / ids / esquema
    • Leer y normalizar todos los archivos de categorias/
    • Reportar estado, inventario y diagnóstico propios
  conocimiento_exportable:
    • categorias
    • ids
    • por_id
    • esquema
    • inventario
    • reporte
    • diagnostico
  consultas_soportadas:
    • listar_ids
    • consultar_por_id
    • obtener_esquema
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • verificar_coherencia
  requiere:
    []
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    modificar: False
    alterar: False
    reescribir: False
  capacidades:
    • verificar
    • barrer
    • inventario
    • categorias
    • por_id
    • ids
    • esquema
    • reporte
    • diagnostico
    • verificar_salida
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia del glosario.
      entrada: ninguna
      salida: dict con coherente, categorias, ids, errores
    barrer:
      descripcion: Evalúa coherencia del glosario de IDs. No calcula.
      entrada: ninguna
      salida: dict con coherente, categorias, ids, errores, esquema
    inventario:
      descripcion: Inventario completo del módulo y de los IDs.
      entrada: peticion opcional
      salida: dict con id, version, categorias, ids, total, errores
    categorias:
      descripcion: Lista del catálogo si coherente; si no, lista vacía.
      entrada: ninguna
      salida: list[dict] de categorías normalizadas
    por_id:
      descripcion: Devuelve la categoría normalizada de un id, o None.
      entrada: cat_id: str
      salida: dict | None
    ids:
      descripcion: Lista de todos los ids del catálogo coherente.
      entrada: ninguna
      salida: list[str]
    esquema:
      descripcion: Esquema de forma de una categoría (obligatorios, opcionales, prohibidos).
      entrada: ninguna
      salida: dict ESQUEMA_CATEGORIA
    reporte:
      descripcion: Reporte interno de estado del módulo CC.
      entrada: ninguna
      salida: dict con estado, coherente, categorias, ids, errores
    diagnostico:
      descripcion: Diagnóstico: qué falta o está mal en el glosario.
      entrada: ninguna
      salida: dict con estado, problemas, advertencias, recomendaciones
    verificar_salida:
      descripcion: Comprueba forma de una salida de barrer: coherente bool, errores list, ids list, categorias int.
      entrada: salida: dict
      salida: bool
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • las capacidades declaradas son siempre callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • este módulo no calcula Tru / C / L / K
    • este módulo no orquesta el ciclo
    • este módulo no envía reportes a otros módulos
    • los IDs viven en categorias/, no en este INIT
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
  reporte:
    id: CC
    modulo: catalogo_citaciones
    rol: CC
    version: 2.1
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: DEGRADADO
    coherente: False
    categorias: 222
    ids:
      • afirmaciones
      • afirmaciones
      • afirmaciones_falsas
      • afirmaciones_falsas
      • alpha
      • alpha
      • aplicar_escala
      • aplicar_escala
      • autoriza_engine
      • autoriza_engine
      • ax
      • ax
      • barrer
      • barrer
      • base_nula
      • base_nula
      • base_nula_c
      • base_nula_c
      • base_nula_k
      • base_nula_k
      • base_nula_l
      • base_nula_l
      • beta
      • beta
      • c
      • c
      • c
      • c
      • ca
      • ca
      • calcular_c
      • calcular_c
      • calcular_k
      • calcular_k
      • calcular_l
      • calcular_l
      • calculator
      • calculator
      • capacidades
      • capacidades
      • capacidades_meta
      • capacidades_meta
      • catalogo_citaciones
      • catalogo_citaciones
      • categorias
      • categorias
      • cc
      • cc
      • coherencia
      • coherencia
      • coherencia_fn
      • coherencia_fn
      • combinar_resultados
      • combinar_resultados
      • compromisos
      • compromisos
      • conocimiento_exportable
      • conocimiento_exportable
      • contenedor
      • contenedor
      • conteos
      • conteos
      • contexto
      • contexto
      • contradicciones
      • contradicciones
      • correlacion_fn
      • correlacion_fn
      • correlacion_k
      • correlacion_k
      • ct
      • ct
      • cx
      • cx
      • decimal
      • decimal
      • degradado
      • degradado
      • denominador
      • denominador
      • descubrir
      • descubrir
      • dg
      • dg
      • diagnostico
      • diagnostico
      • display
      • display
      • ejecutar_capacidad
      • ejecutar_capacidad
      • en
      • en
      • engine
      • engine
      • es_valida
      • es_valida
      • escala
      • escala
      • escalas_ids
      • escalas_ids
      • esquema
      • esquema
      • esquema_categoria
      • esquema_categoria
      • estados_validos
      • estados_validos
      • extraer_conteos
      • extraer_conteos
      • f
      • f
      • fo
      • fo
      • formulas
      • formulas
      • fraccion
      • fraccion
      • ids
      • ids
      • invariantes
      • invariantes
      • inventario
      • inventario
      • inyectar_en_peticion
      • inyectar_en_peticion
      • k
      • k
      • k
      • k
      • l
      • l
      • leer_ids_escala
      • leer_ids_escala
      • logica
      • logica
      • logica_fn
      • logica_fn
      • m
      • m
      • mc
      • mc
      • no_iniciado
      • no_iniciado
      • numerador
      • numerador
      • o_context
      • o_context
      • o_presente
      • o_presente
      • omega
      • omega
      • omegareport
      • omegareport
      • operativo
      • operativo
      • p
      • p
      • por_id
      • por_id
      • posturas
      • posturas
      • precision
      • precision
      • r
      • r
      • rechazado
      • rechazado
      • recolectar
      • recolectar
      • reporte
      • reporte
      • reporting
      • reporting
      • representar
      • representar
      • requiere
      • requiere
      • resolver_dependencias
      • resolver_dependencias
      • resolver_pedido
      • resolver_pedido
      • reversiones
      • reversiones
      • tru_atomo
      • tru_atomo
      • tru_conversacion
      • tru_conversacion
      • tru_frase
      • tru_frase
      • tru_repositorio
      • tru_repositorio
      • tru_ri
      • tru_ri
      • tru_ri
      • tru_ri
      • tru_sujeto
      • tru_sujeto
      • tru_total
      • tru_total
      • tru_total
      • tru_total
      • tru_totales
      • tru_totales
      • truth
      • truth
      • tt
      • tt
      • undefined
      • undefined
      • valor
      • valor
      • verificar
      • verificar
      • verificar_c
      • verificar_c
      • verificar_escala
      • verificar_escala
      • verificar_k
      • verificar_k
      • verificar_l
      • verificar_l
      • verificar_salida
      • verificar_salida
    errores:
      [0]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'ca' en ['ids_sistema', 'ids_sistema']
      [1]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'fo' en ['ids_sistema', 'ids_sistema']
      [2]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tt' en ['ids_sistema', 'ids_sistema']
      [3]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'cc' en ['ids_sistema', 'ids_sistema']
      [4]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'ct' en ['ids_sistema', 'ids_sistema']
      [5]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'ax' en ['ids_sistema', 'ids_sistema']
      [6]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'mc' en ['ids_sistema', 'ids_sistema']
      [7]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'cx' en ['ids_sistema', 'ids_sistema']
      [8]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'dg' en ['ids_sistema', 'ids_sistema']
      [9]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'en' en ['ids_sistema', 'ids_sistema']
      [10]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'calculator' en ['ids_sistema', 'ids_sistema']
      [11]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'coherencia' en ['ids_sistema', 'ids_sistema']
      [12]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'logica' en ['ids_sistema', 'ids_sistema']
      [13]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'correlacion_k' en ['ids_sistema', 'ids_sistema']
      [14]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'conteos' en ['ids_sistema', 'ids_sistema']
      [15]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'escalas_ids' en ['ids_sistema', 'ids_sistema']
      [16]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'formulas' en ['ids_sistema', 'ids_sistema']
      [17]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'truth' en ['ids_sistema', 'ids_sistema']
      [18]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'escala' en ['ids_sistema', 'ids_sistema']
      [19]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_totales' en ['ids_sistema', 'ids_sistema']
      [20]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'catalogo_citaciones' en ['ids_sistema', 'ids_sistema']
      [21]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'coherencia_fn' en ['ids_sistema', 'ids_sistema']
      [22]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'logica_fn' en ['ids_sistema', 'ids_sistema']
      [23]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'correlacion_fn' en ['ids_sistema', 'ids_sistema']
      [24]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'calcular_c' en ['ids_sistema', 'ids_sistema']
      [25]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'calcular_l' en ['ids_sistema', 'ids_sistema']
      [26]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'calcular_k' en ['ids_sistema', 'ids_sistema']
      [27]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar_c' en ['ids_sistema', 'ids_sistema']
      [28]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar_l' en ['ids_sistema', 'ids_sistema']
      [29]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar_k' en ['ids_sistema', 'ids_sistema']
      [30]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'extraer_conteos' en ['ids_sistema', 'ids_sistema']
      [31]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'inyectar_en_peticion' en ['ids_sistema', 'ids_sistema']
      [32]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'leer_ids_escala' en ['ids_sistema', 'ids_sistema']
      [33]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'representar' en ['ids_sistema', 'ids_sistema']
      [34]
        archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
        error: id duplicado 'tru_ri' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
      [35]
        archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
        error: id duplicado 'tru_total' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
      [36]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'aplicar_escala' en ['ids_sistema', 'ids_sistema']
      [37]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar_escala' en ['ids_sistema', 'ids_sistema']
      [38]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'resolver_pedido' en ['ids_sistema', 'ids_sistema']
      [39]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'categorias' en ['ids_sistema', 'ids_sistema']
      [40]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'por_id' en ['ids_sistema', 'ids_sistema']
      [41]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'ids' en ['ids_sistema', 'ids_sistema']
      [42]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'es_valida' en ['ids_sistema', 'ids_sistema']
      [43]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'esquema' en ['ids_sistema', 'ids_sistema']
      [44]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'barrer' en ['ids_sistema', 'ids_sistema']
      [45]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar' en ['ids_sistema', 'ids_sistema']
      [46]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar_salida' en ['ids_sistema', 'ids_sistema']
      [47]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'inventario' en ['ids_sistema', 'ids_sistema']
      [48]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'reporte' en ['ids_sistema', 'ids_sistema']
      [49]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'diagnostico' en ['ids_sistema', 'ids_sistema']
      [50]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'recolectar' en ['ids_sistema', 'ids_sistema']
      [51]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'descubrir' en ['ids_sistema', 'ids_sistema']
      [52]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'resolver_dependencias' en ['ids_sistema', 'ids_sistema']
      [53]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'ejecutar_capacidad' en ['ids_sistema', 'ids_sistema']
      [54]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'combinar_resultados' en ['ids_sistema', 'ids_sistema']
      [55]
        archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
        error: id duplicado 'c' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
      [56]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'l' en ['ids_sistema', 'ids_sistema']
      [57]
        archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
        error: id duplicado 'k' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
      [58]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'alpha' en ['ids_sistema', 'ids_sistema']
      [59]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'beta' en ['ids_sistema', 'ids_sistema']
      [60]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'm' en ['ids_sistema', 'ids_sistema']
      [61]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'p' en ['ids_sistema', 'ids_sistema']
      [62]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'r' en ['ids_sistema', 'ids_sistema']
      [63]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'f' en ['ids_sistema', 'ids_sistema']
      [64]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'compromisos' en ['ids_sistema', 'ids_sistema']
      [65]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'contradicciones' en ['ids_sistema', 'ids_sistema']
      [66]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'posturas' en ['ids_sistema', 'ids_sistema']
      [67]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'reversiones' en ['ids_sistema', 'ids_sistema']
      [68]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'afirmaciones' en ['ids_sistema', 'ids_sistema']
      [69]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'afirmaciones_falsas' en ['ids_sistema', 'ids_sistema']
      [70]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'base_nula' en ['ids_sistema', 'ids_sistema']
      [71]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'base_nula_c' en ['ids_sistema', 'ids_sistema']
      [72]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'base_nula_l' en ['ids_sistema', 'ids_sistema']
      [73]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'base_nula_k' en ['ids_sistema', 'ids_sistema']
      [74]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'o_presente' en ['ids_sistema', 'ids_sistema']
      [75]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'o_context' en ['ids_sistema', 'ids_sistema']
      [76]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'contexto' en ['ids_sistema', 'ids_sistema']
      [77]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'undefined' en ['ids_sistema', 'ids_sistema']
      [78]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_atomo' en ['ids_sistema', 'ids_sistema']
      [79]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_frase' en ['ids_sistema', 'ids_sistema']
      [80]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_sujeto' en ['ids_sistema', 'ids_sistema']
      [81]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_conversacion' en ['ids_sistema', 'ids_sistema']
      [82]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_repositorio' en ['ids_sistema', 'ids_sistema']
      [83]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'fraccion' en ['ids_sistema', 'ids_sistema']
      [84]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'decimal' en ['ids_sistema', 'ids_sistema']
      [85]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'display' en ['ids_sistema', 'ids_sistema']
      [86]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'numerador' en ['ids_sistema', 'ids_sistema']
      [87]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'denominador' en ['ids_sistema', 'ids_sistema']
      [88]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'precision' en ['ids_sistema', 'ids_sistema']
      [89]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'valor' en ['ids_sistema', 'ids_sistema']
      [90]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'contenedor' en ['ids_sistema', 'ids_sistema']
      [91]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'capacidades' en ['ids_sistema', 'ids_sistema']
      [92]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'capacidades_meta' en ['ids_sistema', 'ids_sistema']
      [93]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'autoriza_engine' en ['ids_sistema', 'ids_sistema']
      [94]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'conocimiento_exportable' en ['ids_sistema', 'ids_sistema']
      [95]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'requiere' en ['ids_sistema', 'ids_sistema']
      [96]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'reporting' en ['ids_sistema', 'ids_sistema']
      [97]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'invariantes' en ['ids_sistema', 'ids_sistema']
      [98]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'estados_validos' en ['ids_sistema', 'ids_sistema']
      [99]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'esquema_categoria' en ['ids_sistema', 'ids_sistema']
      [100]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'no_iniciado' en ['ids_sistema', 'ids_sistema']
      [101]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'operativo' en ['ids_sistema', 'ids_sistema']
      [102]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'degradado' en ['ids_sistema', 'ids_sistema']
      [103]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'rechazado' en ['ids_sistema', 'ids_sistema']
      [104]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'engine' en ['ids_sistema', 'ids_sistema']
      [105]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'omega' en ['ids_sistema', 'ids_sistema']
      [106]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'omegareport' en ['ids_sistema', 'ids_sistema']
    notas:
      []
    capacidades:
      • verificar
      • barrer
      • inventario
      • categorias
      • por_id
      • ids
      • esquema
      • reporte
      • diagnostico
      • verificar_salida
    requiere:
      []
    autoridad:
      • Declarar los IDs disponibles en el catálogo
      • Resolver consulta por_id / ids / esquema
      • Leer y normalizar todos los archivos de categorias/
      • Reportar estado, inventario y diagnóstico propios
    conocimiento_exportable:
      • categorias
      • ids
      • por_id
      • esquema
      • inventario
      • reporte
      • diagnostico
    consultas_soportadas:
      • listar_ids
      • consultar_por_id
      • obtener_esquema
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • verificar_coherencia
  diagnostico:
    id: CC
    modulo: catalogo_citaciones
    estado: DEGRADADO
    problemas:
      [0]
        tipo: errores_catalogo
        detalle:
          [0]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'ca' en ['ids_sistema', 'ids_sistema']
          [1]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'fo' en ['ids_sistema', 'ids_sistema']
          [2]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'tt' en ['ids_sistema', 'ids_sistema']
          [3]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'cc' en ['ids_sistema', 'ids_sistema']
          [4]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'ct' en ['ids_sistema', 'ids_sistema']
          [5]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'ax' en ['ids_sistema', 'ids_sistema']
          [6]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'mc' en ['ids_sistema', 'ids_sistema']
          [7]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'cx' en ['ids_sistema', 'ids_sistema']
          [8]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'dg' en ['ids_sistema', 'ids_sistema']
          [9]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'en' en ['ids_sistema', 'ids_sistema']
          [10]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'calculator' en ['ids_sistema', 'ids_sistema']
          [11]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'coherencia' en ['ids_sistema', 'ids_sistema']
          [12]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'logica' en ['ids_sistema', 'ids_sistema']
          [13]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'correlacion_k' en ['ids_sistema', 'ids_sistema']
          [14]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'conteos' en ['ids_sistema', 'ids_sistema']
          [15]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'escalas_ids' en ['ids_sistema', 'ids_sistema']
          [16]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'formulas' en ['ids_sistema', 'ids_sistema']
          [17]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'truth' en ['ids_sistema', 'ids_sistema']
          [18]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'escala' en ['ids_sistema', 'ids_sistema']
          [19]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'tru_totales' en ['ids_sistema', 'ids_sistema']
          [20]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'catalogo_citaciones' en ['ids_sistema', 'ids_sistema']
          [21]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'coherencia_fn' en ['ids_sistema', 'ids_sistema']
          [22]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'logica_fn' en ['ids_sistema', 'ids_sistema']
          [23]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'correlacion_fn' en ['ids_sistema', 'ids_sistema']
          [24]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'calcular_c' en ['ids_sistema', 'ids_sistema']
          [25]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'calcular_l' en ['ids_sistema', 'ids_sistema']
          [26]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'calcular_k' en ['ids_sistema', 'ids_sistema']
          [27]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'verificar_c' en ['ids_sistema', 'ids_sistema']
          [28]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'verificar_l' en ['ids_sistema', 'ids_sistema']
          [29]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'verificar_k' en ['ids_sistema', 'ids_sistema']
          [30]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'extraer_conteos' en ['ids_sistema', 'ids_sistema']
          [31]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'inyectar_en_peticion' en ['ids_sistema', 'ids_sistema']
          [32]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'leer_ids_escala' en ['ids_sistema', 'ids_sistema']
          [33]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'representar' en ['ids_sistema', 'ids_sistema']
          [34]
            archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
            error: id duplicado 'tru_ri' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
          [35]
            archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
            error: id duplicado 'tru_total' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
          [36]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'aplicar_escala' en ['ids_sistema', 'ids_sistema']
          [37]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'verificar_escala' en ['ids_sistema', 'ids_sistema']
          [38]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'resolver_pedido' en ['ids_sistema', 'ids_sistema']
          [39]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'categorias' en ['ids_sistema', 'ids_sistema']
          [40]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'por_id' en ['ids_sistema', 'ids_sistema']
          [41]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'ids' en ['ids_sistema', 'ids_sistema']
          [42]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'es_valida' en ['ids_sistema', 'ids_sistema']
          [43]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'esquema' en ['ids_sistema', 'ids_sistema']
          [44]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'barrer' en ['ids_sistema', 'ids_sistema']
          [45]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'verificar' en ['ids_sistema', 'ids_sistema']
          [46]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'verificar_salida' en ['ids_sistema', 'ids_sistema']
          [47]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'inventario' en ['ids_sistema', 'ids_sistema']
          [48]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'reporte' en ['ids_sistema', 'ids_sistema']
          [49]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'diagnostico' en ['ids_sistema', 'ids_sistema']
          [50]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'recolectar' en ['ids_sistema', 'ids_sistema']
          [51]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'descubrir' en ['ids_sistema', 'ids_sistema']
          [52]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'resolver_dependencias' en ['ids_sistema', 'ids_sistema']
          [53]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'ejecutar_capacidad' en ['ids_sistema', 'ids_sistema']
          [54]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'combinar_resultados' en ['ids_sistema', 'ids_sistema']
          [55]
            archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
            error: id duplicado 'c' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
          [56]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'l' en ['ids_sistema', 'ids_sistema']
          [57]
            archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
            error: id duplicado 'k' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
          [58]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'alpha' en ['ids_sistema', 'ids_sistema']
          [59]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'beta' en ['ids_sistema', 'ids_sistema']
          [60]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'm' en ['ids_sistema', 'ids_sistema']
          [61]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'p' en ['ids_sistema', 'ids_sistema']
          [62]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'r' en ['ids_sistema', 'ids_sistema']
          [63]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'f' en ['ids_sistema', 'ids_sistema']
          [64]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'compromisos' en ['ids_sistema', 'ids_sistema']
          [65]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'contradicciones' en ['ids_sistema', 'ids_sistema']
          [66]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'posturas' en ['ids_sistema', 'ids_sistema']
          [67]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'reversiones' en ['ids_sistema', 'ids_sistema']
          [68]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'afirmaciones' en ['ids_sistema', 'ids_sistema']
          [69]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'afirmaciones_falsas' en ['ids_sistema', 'ids_sistema']
          [70]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'base_nula' en ['ids_sistema', 'ids_sistema']
          [71]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'base_nula_c' en ['ids_sistema', 'ids_sistema']
          [72]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'base_nula_l' en ['ids_sistema', 'ids_sistema']
          [73]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'base_nula_k' en ['ids_sistema', 'ids_sistema']
          [74]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'o_presente' en ['ids_sistema', 'ids_sistema']
          [75]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'o_context' en ['ids_sistema', 'ids_sistema']
          [76]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'contexto' en ['ids_sistema', 'ids_sistema']
          [77]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'undefined' en ['ids_sistema', 'ids_sistema']
          [78]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'tru_atomo' en ['ids_sistema', 'ids_sistema']
          [79]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'tru_frase' en ['ids_sistema', 'ids_sistema']
          [80]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'tru_sujeto' en ['ids_sistema', 'ids_sistema']
          [81]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'tru_conversacion' en ['ids_sistema', 'ids_sistema']
          [82]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'tru_repositorio' en ['ids_sistema', 'ids_sistema']
          [83]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'fraccion' en ['ids_sistema', 'ids_sistema']
          [84]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'decimal' en ['ids_sistema', 'ids_sistema']
          [85]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'display' en ['ids_sistema', 'ids_sistema']
          [86]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'numerador' en ['ids_sistema', 'ids_sistema']
          [87]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'denominador' en ['ids_sistema', 'ids_sistema']
          [88]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'precision' en ['ids_sistema', 'ids_sistema']
          [89]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'valor' en ['ids_sistema', 'ids_sistema']
          [90]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'contenedor' en ['ids_sistema', 'ids_sistema']
          [91]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'capacidades' en ['ids_sistema', 'ids_sistema']
          [92]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'capacidades_meta' en ['ids_sistema', 'ids_sistema']
          [93]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'autoriza_engine' en ['ids_sistema', 'ids_sistema']
          [94]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'conocimiento_exportable' en ['ids_sistema', 'ids_sistema']
          [95]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'requiere' en ['ids_sistema', 'ids_sistema']
          [96]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'reporting' en ['ids_sistema', 'ids_sistema']
          [97]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'invariantes' en ['ids_sistema', 'ids_sistema']
          [98]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'estados_validos' en ['ids_sistema', 'ids_sistema']
          [99]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'esquema_categoria' en ['ids_sistema', 'ids_sistema']
          [100]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'no_iniciado' en ['ids_sistema', 'ids_sistema']
          [101]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'operativo' en ['ids_sistema', 'ids_sistema']
          [102]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'degradado' en ['ids_sistema', 'ids_sistema']
          [103]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'rechazado' en ['ids_sistema', 'ids_sistema']
          [104]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'engine' en ['ids_sistema', 'ids_sistema']
          [105]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'omega' en ['ids_sistema', 'ids_sistema']
          [106]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'omegareport' en ['ids_sistema', 'ids_sistema']
    advertencias:
      []
    recomendaciones:
      • Corregir archivos de categorias/ con errores de forma o carga
    coherente: False
    errores_n: 107
    categorias_n: 222
  inventario:
    id: CC
    nombre: catalogo_citaciones
    rol: CC
    version: 2.1
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    funcion: Glosario de IDs del repositorio. Expone ids a Engine para citar/reportar. No calcula.
    uso:
      • consulta de IDs
      • resolución por id
      • esquema de categorías
    esquema_categoria:
      obligatorios:
        • id
        • nombre
        • unidad
        • enunciado
      opcionales:
        • nivel_fractal
        • jurisdiccion
        • requiere
        • factores_evaluables
        • agrega_desde
        • fuente_modulo
        • senales
        • anclas
        • version
        • notas
      prohibidos:
        • Tru_Ri
        • Tru_total
        • tru_ri
        • tru_total
        • C
        • L
        • K
        • alpha
        • beta
        • ALPHA
        • BETA
        • Fraction
      nota: Archivos bajo categorias/ declaran CATEGORIA o CATEGORIAS o IDS. Cada uno aporta uno o más IDs del repositorio. CC los lee y expone. No calcula. Este INIT no embebe IDs.
    categorias:
      [0]
        id: afirmaciones
        nombre: afirmaciones
        unidad: clave
        enunciado: Clave de conteo: afirmaciones
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [1]
        id: afirmaciones
        nombre: afirmaciones
        unidad: id
        enunciado: ID del repositorio: afirmaciones
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [2]
        id: afirmaciones_falsas
        nombre: afirmaciones_falsas
        unidad: clave
        enunciado: Clave de conteo: afirmaciones_falsas
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [3]
        id: afirmaciones_falsas
        nombre: afirmaciones_falsas
        unidad: id
        enunciado: ID del repositorio: afirmaciones_falsas
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [4]
        id: alpha
        nombre: ALPHA
        unidad: factor
        enunciado: Factor o magnitud: ALPHA
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [5]
        id: alpha
        nombre: ALPHA
        unidad: id
        enunciado: ID del repositorio: ALPHA
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [6]
        id: aplicar_escala
        nombre: aplicar_escala
        unidad: funcion
        enunciado: Función o capacidad: aplicar_escala
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [7]
        id: aplicar_escala
        nombre: aplicar_escala
        unidad: id
        enunciado: ID del repositorio: aplicar_escala
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [8]
        id: autoriza_engine
        nombre: autoriza_engine
        unidad: campo
        enunciado: Campo estructural de contrato: autoriza_engine
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [9]
        id: autoriza_engine
        nombre: autoriza_engine
        unidad: id
        enunciado: ID del repositorio: autoriza_engine
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [10]
        id: ax
        nombre: AX
        unidad: rol
        enunciado: Módulo / rol del sistema: AX
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [11]
        id: ax
        nombre: AX
        unidad: id
        enunciado: ID del repositorio: AX
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [12]
        id: barrer
        nombre: barrer
        unidad: funcion
        enunciado: Función o capacidad: barrer
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [13]
        id: barrer
        nombre: barrer
        unidad: id
        enunciado: ID del repositorio: barrer
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [14]
        id: base_nula
        nombre: base_nula
        unidad: meta
        enunciado: Metadato de dominio: base_nula
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [15]
        id: base_nula
        nombre: base_nula
        unidad: id
        enunciado: ID del repositorio: base_nula
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [16]
        id: base_nula_c
        nombre: base_nula_C
        unidad: meta
        enunciado: Metadato de dominio: base_nula_C
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [17]
        id: base_nula_c
        nombre: base_nula_C
        unidad: id
        enunciado: ID del repositorio: base_nula_C
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [18]
        id: base_nula_k
        nombre: base_nula_K
        unidad: meta
        enunciado: Metadato de dominio: base_nula_K
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [19]
        id: base_nula_k
        nombre: base_nula_K
        unidad: id
        enunciado: ID del repositorio: base_nula_K
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [20]
        id: base_nula_l
        nombre: base_nula_L
        unidad: meta
        enunciado: Metadato de dominio: base_nula_L
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [21]
        id: base_nula_l
        nombre: base_nula_L
        unidad: id
        enunciado: ID del repositorio: base_nula_L
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [22]
        id: beta
        nombre: BETA
        unidad: factor
        enunciado: Factor o magnitud: BETA
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [23]
        id: beta
        nombre: BETA
        unidad: id
        enunciado: ID del repositorio: BETA
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [24]
        id: c
        nombre: C
        unidad: factor
        enunciado: Factor o magnitud: C
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [25]
        id: c
        nombre: c
        unidad: variable
        enunciado: Variable matemática: c
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=variable
      [26]
        id: c
        nombre: C
        unidad: id
        enunciado: ID del repositorio: C
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [27]
        id: c
        nombre: c
        unidad: id
        enunciado: ID del repositorio: c
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [28]
        id: ca
        nombre: CA
        unidad: rol
        enunciado: Módulo / rol del sistema: CA
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [29]
        id: ca
        nombre: CA
        unidad: id
        enunciado: ID del repositorio: CA
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [30]
        id: calcular_c
        nombre: calcular_c
        unidad: funcion
        enunciado: Función o capacidad: calcular_c
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [31]
        id: calcular_c
        nombre: calcular_c
        unidad: id
        enunciado: ID del repositorio: calcular_c
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [32]
        id: calcular_k
        nombre: calcular_k
        unidad: funcion
        enunciado: Función o capacidad: calcular_k
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [33]
        id: calcular_k
        nombre: calcular_k
        unidad: id
        enunciado: ID del repositorio: calcular_k
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [34]
        id: calcular_l
        nombre: calcular_l
        unidad: funcion
        enunciado: Función o capacidad: calcular_l
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [35]
        id: calcular_l
        nombre: calcular_l
        unidad: id
        enunciado: ID del repositorio: calcular_l
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [36]
        id: calculator
        nombre: calculator
        unidad: archivo
        enunciado: Archivo del repositorio: calculator
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [37]
        id: calculator
        nombre: calculator
        unidad: id
        enunciado: ID del repositorio: calculator
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [38]
        id: capacidades
        nombre: capacidades
        unidad: campo
        enunciado: Campo estructural de contrato: capacidades
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [39]
        id: capacidades
        nombre: capacidades
        unidad: id
        enunciado: ID del repositorio: capacidades
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [40]
        id: capacidades_meta
        nombre: capacidades_meta
        unidad: campo
        enunciado: Campo estructural de contrato: capacidades_meta
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [41]
        id: capacidades_meta
        nombre: capacidades_meta
        unidad: id
        enunciado: ID del repositorio: capacidades_meta
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [42]
        id: catalogo_citaciones
        nombre: catalogo_citaciones
        unidad: archivo
        enunciado: Archivo del repositorio: catalogo_citaciones
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [43]
        id: catalogo_citaciones
        nombre: catalogo_citaciones
        unidad: id
        enunciado: ID del repositorio: catalogo_citaciones
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [44]
        id: categorias
        nombre: categorias
        unidad: funcion
        enunciado: Función o capacidad: categorias
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [45]
        id: categorias
        nombre: categorias
        unidad: id
        enunciado: ID del repositorio: categorias
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [46]
        id: cc
        nombre: CC
        unidad: rol
        enunciado: Módulo / rol del sistema: CC
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [47]
        id: cc
        nombre: CC
        unidad: id
        enunciado: ID del repositorio: CC
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [48]
        id: coherencia
        nombre: coherencia
        unidad: archivo
        enunciado: Archivo del repositorio: coherencia
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [49]
        id: coherencia
        nombre: coherencia
        unidad: id
        enunciado: ID del repositorio: coherencia
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [50]
        id: coherencia_fn
        nombre: coherencia_fn
        unidad: funcion
        enunciado: Función o capacidad: coherencia_fn
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [51]
        id: coherencia_fn
        nombre: coherencia_fn
        unidad: id
        enunciado: ID del repositorio: coherencia_fn
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [52]
        id: combinar_resultados
        nombre: combinar_resultados
        unidad: funcion
        enunciado: Función o capacidad: combinar_resultados
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [53]
        id: combinar_resultados
        nombre: combinar_resultados
        unidad: id
        enunciado: ID del repositorio: combinar_resultados
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [54]
        id: compromisos
        nombre: compromisos
        unidad: clave
        enunciado: Clave de conteo: compromisos
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [55]
        id: compromisos
        nombre: compromisos
        unidad: id
        enunciado: ID del repositorio: compromisos
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [56]
        id: conocimiento_exportable
        nombre: conocimiento_exportable
        unidad: campo
        enunciado: Campo estructural de contrato: conocimiento_exportable
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [57]
        id: conocimiento_exportable
        nombre: conocimiento_exportable
        unidad: id
        enunciado: ID del repositorio: conocimiento_exportable
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [58]
        id: contenedor
        nombre: CONTENEDOR
        unidad: campo
        enunciado: Campo estructural de contrato: CONTENEDOR
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [59]
        id: contenedor
        nombre: CONTENEDOR
        unidad: id
        enunciado: ID del repositorio: CONTENEDOR
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [60]
        id: conteos
        nombre: conteos
        unidad: archivo
        enunciado: Archivo del repositorio: conteos
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [61]
        id: conteos
        nombre: conteos
        unidad: id
        enunciado: ID del repositorio: conteos
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [62]
        id: contexto
        nombre: contexto
        unidad: meta
        enunciado: Metadato de dominio: contexto
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [63]
        id: contexto
        nombre: contexto
        unidad: id
        enunciado: ID del repositorio: contexto
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [64]
        id: contradicciones
        nombre: contradicciones
        unidad: clave
        enunciado: Clave de conteo: contradicciones
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [65]
        id: contradicciones
        nombre: contradicciones
        unidad: id
        enunciado: ID del repositorio: contradicciones
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [66]
        id: correlacion_fn
        nombre: correlacion_fn
        unidad: funcion
        enunciado: Función o capacidad: correlacion_fn
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [67]
        id: correlacion_fn
        nombre: correlacion_fn
        unidad: id
        enunciado: ID del repositorio: correlacion_fn
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [68]
        id: correlacion_k
        nombre: correlacion_k
        unidad: archivo
        enunciado: Archivo del repositorio: correlacion_k
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [69]
        id: correlacion_k
        nombre: correlacion_k
        unidad: id
        enunciado: ID del repositorio: correlacion_k
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [70]
        id: ct
        nombre: CT
        unidad: rol
        enunciado: Módulo / rol del sistema: CT
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [71]
        id: ct
        nombre: CT
        unidad: id
        enunciado: ID del repositorio: CT
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [72]
        id: cx
        nombre: CX
        unidad: rol
        enunciado: Módulo / rol del sistema: CX
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [73]
        id: cx
        nombre: CX
        unidad: id
        enunciado: ID del repositorio: CX
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [74]
        id: decimal
        nombre: decimal
        unidad: campo
        enunciado: Campo de representación: decimal
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [75]
        id: decimal
        nombre: decimal
        unidad: id
        enunciado: ID del repositorio: decimal
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [76]
        id: degradado
        nombre: DEGRADADO
        unidad: estado
        enunciado: Estado de módulo: DEGRADADO
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=estado
      [77]
        id: degradado
        nombre: DEGRADADO
        unidad: id
        enunciado: ID del repositorio: DEGRADADO
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [78]
        id: denominador
        nombre: denominador
        unidad: campo
        enunciado: Campo de representación: denominador
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [79]
        id: denominador
        nombre: denominador
        unidad: id
        enunciado: ID del repositorio: denominador
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [80]
        id: descubrir
        nombre: descubrir
        unidad: funcion
        enunciado: Función o capacidad: descubrir
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [81]
        id: descubrir
        nombre: descubrir
        unidad: id
        enunciado: ID del repositorio: descubrir
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [82]
        id: dg
        nombre: DG
        unidad: rol
        enunciado: Módulo / rol del sistema: DG
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [83]
        id: dg
        nombre: DG
        unidad: id
        enunciado: ID del repositorio: DG
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [84]
        id: diagnostico
        nombre: diagnostico
        unidad: funcion
        enunciado: Función o capacidad: diagnostico
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [85]
        id: diagnostico
        nombre: diagnostico
        unidad: id
        enunciado: ID del repositorio: diagnostico
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [86]
        id: display
        nombre: display
        unidad: campo
        enunciado: Campo de representación: display
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [87]
        id: display
        nombre: display
        unidad: id
        enunciado: ID del repositorio: display
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [88]
        id: ejecutar_capacidad
        nombre: ejecutar_capacidad
        unidad: funcion
        enunciado: Función o capacidad: ejecutar_capacidad
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [89]
        id: ejecutar_capacidad
        nombre: ejecutar_capacidad
        unidad: id
        enunciado: ID del repositorio: ejecutar_capacidad
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [90]
        id: en
        nombre: EN
        unidad: rol
        enunciado: Módulo / rol del sistema: EN
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [91]
        id: en
        nombre: EN
        unidad: id
        enunciado: ID del repositorio: EN
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [92]
        id: engine
        nombre: Engine
        unidad: agente
        enunciado: Agente del sistema: Engine
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=agente
      [93]
        id: engine
        nombre: Engine
        unidad: id
        enunciado: ID del repositorio: Engine
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [94]
        id: es_valida
        nombre: es_valida
        unidad: funcion
        enunciado: Función o capacidad: es_valida
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [95]
        id: es_valida
        nombre: es_valida
        unidad: id
        enunciado: ID del repositorio: es_valida
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [96]
        id: escala
        nombre: escala
        unidad: archivo
        enunciado: Archivo del repositorio: escala
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [97]
        id: escala
        nombre: escala
        unidad: id
        enunciado: ID del repositorio: escala
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [98]
        id: escalas_ids
        nombre: escalas_ids
        unidad: archivo
        enunciado: Archivo del repositorio: escalas_ids
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [99]
        id: escalas_ids
        nombre: escalas_ids
        unidad: id
        enunciado: ID del repositorio: escalas_ids
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [100]
        id: esquema
        nombre: esquema
        unidad: funcion
        enunciado: Función o capacidad: esquema
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [101]
        id: esquema
        nombre: esquema
        unidad: id
        enunciado: ID del repositorio: esquema
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [102]
        id: esquema_categoria
        nombre: ESQUEMA_CATEGORIA
        unidad: campo
        enunciado: Campo estructural de contrato: ESQUEMA_CATEGORIA
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [103]
        id: esquema_categoria
        nombre: ESQUEMA_CATEGORIA
        unidad: id
        enunciado: ID del repositorio: ESQUEMA_CATEGORIA
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [104]
        id: estados_validos
        nombre: estados_validos
        unidad: campo
        enunciado: Campo estructural de contrato: estados_validos
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [105]
        id: estados_validos
        nombre: estados_validos
        unidad: id
        enunciado: ID del repositorio: estados_validos
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [106]
        id: extraer_conteos
        nombre: extraer_conteos
        unidad: funcion
        enunciado: Función o capacidad: extraer_conteos
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [107]
        id: extraer_conteos
        nombre: extraer_conteos
        unidad: id
        enunciado: ID del repositorio: extraer_conteos
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [108]
        id: f
        nombre: f
        unidad: variable
        enunciado: Variable matemática: f
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=variable
      [109]
        id: f
        nombre: f
        unidad: id
        enunciado: ID del repositorio: f
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [110]
        id: fo
        nombre: FO
        unidad: rol
        enunciado: Módulo / rol del sistema: FO
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [111]
        id: fo
        nombre: FO
        unidad: id
        enunciado: ID del repositorio: FO
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [112]
        id: formulas
        nombre: formulas
        unidad: archivo
        enunciado: Archivo del repositorio: formulas
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [113]
        id: formulas
        nombre: formulas
        unidad: id
        enunciado: ID del repositorio: formulas
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [114]
        id: fraccion
        nombre: fraccion
        unidad: campo
        enunciado: Campo de representación: fraccion
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [115]
        id: fraccion
        nombre: fraccion
        unidad: id
        enunciado: ID del repositorio: fraccion
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [116]
        id: ids
        nombre: ids
        unidad: funcion
        enunciado: Función o capacidad: ids
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [117]
        id: ids
        nombre: ids
        unidad: id
        enunciado: ID del repositorio: ids
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [118]
        id: invariantes
        nombre: invariantes
        unidad: campo
        enunciado: Campo estructural de contrato: invariantes
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [119]
        id: invariantes
        nombre: invariantes
        unidad: id
        enunciado: ID del repositorio: invariantes
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [120]
        id: inventario
        nombre: inventario
        unidad: funcion
        enunciado: Función o capacidad: inventario
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [121]
        id: inventario
        nombre: inventario
        unidad: id
        enunciado: ID del repositorio: inventario
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [122]
        id: inyectar_en_peticion
        nombre: inyectar_en_peticion
        unidad: funcion
        enunciado: Función o capacidad: inyectar_en_peticion
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [123]
        id: inyectar_en_peticion
        nombre: inyectar_en_peticion
        unidad: id
        enunciado: ID del repositorio: inyectar_en_peticion
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [124]
        id: k
        nombre: K
        unidad: factor
        enunciado: Factor o magnitud: K
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [125]
        id: k
        nombre: k
        unidad: variable
        enunciado: Variable matemática: k
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=variable
      [126]
        id: k
        nombre: K
        unidad: id
        enunciado: ID del repositorio: K
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [127]
        id: k
        nombre: k
        unidad: id
        enunciado: ID del repositorio: k
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [128]
        id: l
        nombre: L
        unidad: factor
        enunciado: Factor o magnitud: L
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [129]
        id: l
        nombre: L
        unidad: id
        enunciado: ID del repositorio: L
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [130]
        id: leer_ids_escala
        nombre: leer_ids_escala
        unidad: funcion
        enunciado: Función o capacidad: leer_ids_escala
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [131]
        id: leer_ids_escala
        nombre: leer_ids_escala
        unidad: id
        enunciado: ID del repositorio: leer_ids_escala
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [132]
        id: logica
        nombre: logica
        unidad: archivo
        enunciado: Archivo del repositorio: logica
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [133]
        id: logica
        nombre: logica
        unidad: id
        enunciado: ID del repositorio: logica
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [134]
        id: logica_fn
        nombre: logica_fn
        unidad: funcion
        enunciado: Función o capacidad: logica_fn
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [135]
        id: logica_fn
        nombre: logica_fn
        unidad: id
        enunciado: ID del repositorio: logica_fn
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [136]
        id: m
        nombre: m
        unidad: variable
        enunciado: Variable matemática: m
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=variable
      [137]
        id: m
        nombre: m
        unidad: id
        enunciado: ID del repositorio: m
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [138]
        id: mc
        nombre: MC
        unidad: rol
        enunciado: Módulo / rol del sistema: MC
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [139]
        id: mc
        nombre: MC
        unidad: id
        enunciado: ID del repositorio: MC
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [140]
        id: no_iniciado
        nombre: NO_INICIADO
        unidad: estado
        enunciado: Estado de módulo: NO_INICIADO
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=estado
      [141]
        id: no_iniciado
        nombre: NO_INICIADO
        unidad: id
        enunciado: ID del repositorio: NO_INICIADO
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [142]
        id: numerador
        nombre: numerador
        unidad: campo
        enunciado: Campo de representación: numerador
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [143]
        id: numerador
        nombre: numerador
        unidad: id
        enunciado: ID del repositorio: numerador
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [144]
        id: o_context
        nombre: O_context
        unidad: meta
        enunciado: Metadato de dominio: O_context
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [145]
        id: o_context
        nombre: O_context
        unidad: id
        enunciado: ID del repositorio: O_context
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [146]
        id: o_presente
        nombre: o_presente
        unidad: meta
        enunciado: Metadato de dominio: o_presente
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [147]
        id: o_presente
        nombre: o_presente
        unidad: id
        enunciado: ID del repositorio: o_presente
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [148]
        id: omega
        nombre: Omega
        unidad: agente
        enunciado: Agente del sistema: Omega
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=agente
      [149]
        id: omega
        nombre: Omega
        unidad: id
        enunciado: ID del repositorio: Omega
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [150]
        id: omegareport
        nombre: OmegaReport
        unidad: agente
        enunciado: Agente del sistema: OmegaReport
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=agente
      [151]
        id: omegareport
        nombre: OmegaReport
        unidad: id
        enunciado: ID del repositorio: OmegaReport
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [152]
        id: operativo
        nombre: OPERATIVO
        unidad: estado
        enunciado: Estado de módulo: OPERATIVO
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=estado
      [153]
        id: operativo
        nombre: OPERATIVO
        unidad: id
        enunciado: ID del repositorio: OPERATIVO
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [154]
        id: p
        nombre: p
        unidad: variable
        enunciado: Variable matemática: p
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=variable
      [155]
        id: p
        nombre: p
        unidad: id
        enunciado: ID del repositorio: p
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [156]
        id: por_id
        nombre: por_id
        unidad: funcion
        enunciado: Función o capacidad: por_id
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [157]
        id: por_id
        nombre: por_id
        unidad: id
        enunciado: ID del repositorio: por_id
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [158]
        id: posturas
        nombre: posturas
        unidad: clave
        enunciado: Clave de conteo: posturas
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [159]
        id: posturas
        nombre: posturas
        unidad: id
        enunciado: ID del repositorio: posturas
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [160]
        id: precision
        nombre: precision
        unidad: campo
        enunciado: Campo de representación: precision
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [161]
        id: precision
        nombre: precision
        unidad: id
        enunciado: ID del repositorio: precision
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [162]
        id: r
        nombre: r
        unidad: variable
        enunciado: Variable matemática: r
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=variable
      [163]
        id: r
        nombre: r
        unidad: id
        enunciado: ID del repositorio: r
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [164]
        id: rechazado
        nombre: RECHAZADO
        unidad: estado
        enunciado: Estado de módulo: RECHAZADO
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=estado
      [165]
        id: rechazado
        nombre: RECHAZADO
        unidad: id
        enunciado: ID del repositorio: RECHAZADO
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [166]
        id: recolectar
        nombre: recolectar
        unidad: funcion
        enunciado: Función o capacidad: recolectar
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [167]
        id: recolectar
        nombre: recolectar
        unidad: id
        enunciado: ID del repositorio: recolectar
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [168]
        id: reporte
        nombre: reporte
        unidad: funcion
        enunciado: Función o capacidad: reporte
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [169]
        id: reporte
        nombre: reporte
        unidad: id
        enunciado: ID del repositorio: reporte
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [170]
        id: reporting
        nombre: reporting
        unidad: campo
        enunciado: Campo estructural de contrato: reporting
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [171]
        id: reporting
        nombre: reporting
        unidad: id
        enunciado: ID del repositorio: reporting
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [172]
        id: representar
        nombre: representar
        unidad: funcion
        enunciado: Función o capacidad: representar
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [173]
        id: representar
        nombre: representar
        unidad: id
        enunciado: ID del repositorio: representar
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [174]
        id: requiere
        nombre: requiere
        unidad: campo
        enunciado: Campo estructural de contrato: requiere
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [175]
        id: requiere
        nombre: requiere
        unidad: id
        enunciado: ID del repositorio: requiere
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [176]
        id: resolver_dependencias
        nombre: resolver_dependencias
        unidad: funcion
        enunciado: Función o capacidad: resolver_dependencias
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [177]
        id: resolver_dependencias
        nombre: resolver_dependencias
        unidad: id
        enunciado: ID del repositorio: resolver_dependencias
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [178]
        id: resolver_pedido
        nombre: resolver_pedido
        unidad: funcion
        enunciado: Función o capacidad: resolver_pedido
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [179]
        id: resolver_pedido
        nombre: resolver_pedido
        unidad: id
        enunciado: ID del repositorio: resolver_pedido
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [180]
        id: reversiones
        nombre: reversiones
        unidad: clave
        enunciado: Clave de conteo: reversiones
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [181]
        id: reversiones
        nombre: reversiones
        unidad: id
        enunciado: ID del repositorio: reversiones
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [182]
        id: tru_atomo
        nombre: tru_atomo
        unidad: escala
        enunciado: Escala de alcance Tru: tru_atomo
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=escala
      [183]
        id: tru_atomo
        nombre: tru_atomo
        unidad: id
        enunciado: ID del repositorio: tru_atomo
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [184]
        id: tru_conversacion
        nombre: tru_conversacion
        unidad: escala
        enunciado: Escala de alcance Tru: tru_conversacion
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=escala
      [185]
        id: tru_conversacion
        nombre: tru_conversacion
        unidad: id
        enunciado: ID del repositorio: tru_conversacion
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [186]
        id: tru_frase
        nombre: tru_frase
        unidad: escala
        enunciado: Escala de alcance Tru: tru_frase
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=escala
      [187]
        id: tru_frase
        nombre: tru_frase
        unidad: id
        enunciado: ID del repositorio: tru_frase
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [188]
        id: tru_repositorio
        nombre: tru_repositorio
        unidad: escala
        enunciado: Escala de alcance Tru: tru_repositorio
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=escala
      [189]
        id: tru_repositorio
        nombre: tru_repositorio
        unidad: id
        enunciado: ID del repositorio: tru_repositorio
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [190]
        id: tru_ri
        nombre: tru_ri
        unidad: funcion
        enunciado: Función o capacidad: tru_ri
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [191]
        id: tru_ri
        nombre: Tru_Ri
        unidad: factor
        enunciado: Factor o magnitud: Tru_Ri
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [192]
        id: tru_ri
        nombre: tru_ri
        unidad: id
        enunciado: ID del repositorio: tru_ri
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [193]
        id: tru_ri
        nombre: Tru_Ri
        unidad: id
        enunciado: ID del repositorio: Tru_Ri
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [194]
        id: tru_sujeto
        nombre: tru_sujeto
        unidad: escala
        enunciado: Escala de alcance Tru: tru_sujeto
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=escala
      [195]
        id: tru_sujeto
        nombre: tru_sujeto
        unidad: id
        enunciado: ID del repositorio: tru_sujeto
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [196]
        id: tru_total
        nombre: tru_total
        unidad: funcion
        enunciado: Función o capacidad: tru_total
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [197]
        id: tru_total
        nombre: Tru_total
        unidad: factor
        enunciado: Factor o magnitud: Tru_total
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [198]
        id: tru_total
        nombre: tru_total
        unidad: id
        enunciado: ID del repositorio: tru_total
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [199]
        id: tru_total
        nombre: Tru_total
        unidad: id
        enunciado: ID del repositorio: Tru_total
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [200]
        id: tru_totales
        nombre: tru_totales
        unidad: archivo
        enunciado: Archivo del repositorio: tru_totales
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [201]
        id: tru_totales
        nombre: tru_totales
        unidad: id
        enunciado: ID del repositorio: tru_totales
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [202]
        id: truth
        nombre: truth
        unidad: archivo
        enunciado: Archivo del repositorio: truth
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [203]
        id: truth
        nombre: truth
        unidad: id
        enunciado: ID del repositorio: truth
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [204]
        id: tt
        nombre: TT
        unidad: rol
        enunciado: Módulo / rol del sistema: TT
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [205]
        id: tt
        nombre: TT
        unidad: id
        enunciado: ID del repositorio: TT
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [206]
        id: undefined
        nombre: UNDEFINED
        unidad: meta
        enunciado: Metadato de dominio: UNDEFINED
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [207]
        id: undefined
        nombre: UNDEFINED
        unidad: id
        enunciado: ID del repositorio: UNDEFINED
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [208]
        id: valor
        nombre: valor
        unidad: campo
        enunciado: Campo de representación: valor
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [209]
        id: valor
        nombre: valor
        unidad: id
        enunciado: ID del repositorio: valor
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [210]
        id: verificar
        nombre: verificar
        unidad: funcion
        enunciado: Función o capacidad: verificar
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [211]
        id: verificar
        nombre: verificar
        unidad: id
        enunciado: ID del repositorio: verificar
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [212]
        id: verificar_c
        nombre: verificar_c
        unidad: funcion
        enunciado: Función o capacidad: verificar_c
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [213]
        id: verificar_c
        nombre: verificar_c
        unidad: id
        enunciado: ID del repositorio: verificar_c
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [214]
        id: verificar_escala
        nombre: verificar_escala
        unidad: funcion
        enunciado: Función o capacidad: verificar_escala
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [215]
        id: verificar_escala
        nombre: verificar_escala
        unidad: id
        enunciado: ID del repositorio: verificar_escala
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [216]
        id: verificar_k
        nombre: verificar_k
        unidad: funcion
        enunciado: Función o capacidad: verificar_k
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [217]
        id: verificar_k
        nombre: verificar_k
        unidad: id
        enunciado: ID del repositorio: verificar_k
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [218]
        id: verificar_l
        nombre: verificar_l
        unidad: funcion
        enunciado: Función o capacidad: verificar_l
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [219]
        id: verificar_l
        nombre: verificar_l
        unidad: id
        enunciado: ID del repositorio: verificar_l
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
      [220]
        id: verificar_salida
        nombre: verificar_salida
        unidad: funcion
        enunciado: Función o capacidad: verificar_salida
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [221]
        id: verificar_salida
        nombre: verificar_salida
        unidad: id
        enunciado: ID del repositorio: verificar_salida
        nivel_fractal: NO ENTREGADO POR ENGINE
        jurisdiccion: NO ENTREGADO POR ENGINE
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: NO ENTREGADO POR ENGINE
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: NO ENTREGADO POR ENGINE
    ids:
      • afirmaciones
      • afirmaciones
      • afirmaciones_falsas
      • afirmaciones_falsas
      • alpha
      • alpha
      • aplicar_escala
      • aplicar_escala
      • autoriza_engine
      • autoriza_engine
      • ax
      • ax
      • barrer
      • barrer
      • base_nula
      • base_nula
      • base_nula_c
      • base_nula_c
      • base_nula_k
      • base_nula_k
      • base_nula_l
      • base_nula_l
      • beta
      • beta
      • c
      • c
      • c
      • c
      • ca
      • ca
      • calcular_c
      • calcular_c
      • calcular_k
      • calcular_k
      • calcular_l
      • calcular_l
      • calculator
      • calculator
      • capacidades
      • capacidades
      • capacidades_meta
      • capacidades_meta
      • catalogo_citaciones
      • catalogo_citaciones
      • categorias
      • categorias
      • cc
      • cc
      • coherencia
      • coherencia
      • coherencia_fn
      • coherencia_fn
      • combinar_resultados
      • combinar_resultados
      • compromisos
      • compromisos
      • conocimiento_exportable
      • conocimiento_exportable
      • contenedor
      • contenedor
      • conteos
      • conteos
      • contexto
      • contexto
      • contradicciones
      • contradicciones
      • correlacion_fn
      • correlacion_fn
      • correlacion_k
      • correlacion_k
      • ct
      • ct
      • cx
      • cx
      • decimal
      • decimal
      • degradado
      • degradado
      • denominador
      • denominador
      • descubrir
      • descubrir
      • dg
      • dg
      • diagnostico
      • diagnostico
      • display
      • display
      • ejecutar_capacidad
      • ejecutar_capacidad
      • en
      • en
      • engine
      • engine
      • es_valida
      • es_valida
      • escala
      • escala
      • escalas_ids
      • escalas_ids
      • esquema
      • esquema
      • esquema_categoria
      • esquema_categoria
      • estados_validos
      • estados_validos
      • extraer_conteos
      • extraer_conteos
      • f
      • f
      • fo
      • fo
      • formulas
      • formulas
      • fraccion
      • fraccion
      • ids
      • ids
      • invariantes
      • invariantes
      • inventario
      • inventario
      • inyectar_en_peticion
      • inyectar_en_peticion
      • k
      • k
      • k
      • k
      • l
      • l
      • leer_ids_escala
      • leer_ids_escala
      • logica
      • logica
      • logica_fn
      • logica_fn
      • m
      • m
      • mc
      • mc
      • no_iniciado
      • no_iniciado
      • numerador
      • numerador
      • o_context
      • o_context
      • o_presente
      • o_presente
      • omega
      • omega
      • omegareport
      • omegareport
      • operativo
      • operativo
      • p
      • p
      • por_id
      • por_id
      • posturas
      • posturas
      • precision
      • precision
      • r
      • r
      • rechazado
      • rechazado
      • recolectar
      • recolectar
      • reporte
      • reporte
      • reporting
      • reporting
      • representar
      • representar
      • requiere
      • requiere
      • resolver_dependencias
      • resolver_dependencias
      • resolver_pedido
      • resolver_pedido
      • reversiones
      • reversiones
      • tru_atomo
      • tru_atomo
      • tru_conversacion
      • tru_conversacion
      • tru_frase
      • tru_frase
      • tru_repositorio
      • tru_repositorio
      • tru_ri
      • tru_ri
      • tru_ri
      • tru_ri
      • tru_sujeto
      • tru_sujeto
      • tru_total
      • tru_total
      • tru_total
      • tru_total
      • tru_totales
      • tru_totales
      • truth
      • truth
      • tt
      • tt
      • undefined
      • undefined
      • valor
      • valor
      • verificar
      • verificar
      • verificar_c
      • verificar_c
      • verificar_escala
      • verificar_escala
      • verificar_k
      • verificar_k
      • verificar_l
      • verificar_l
      • verificar_salida
      • verificar_salida
    total: 222
    errores:
      [0]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'ca' en ['ids_sistema', 'ids_sistema']
      [1]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'fo' en ['ids_sistema', 'ids_sistema']
      [2]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tt' en ['ids_sistema', 'ids_sistema']
      [3]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'cc' en ['ids_sistema', 'ids_sistema']
      [4]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'ct' en ['ids_sistema', 'ids_sistema']
      [5]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'ax' en ['ids_sistema', 'ids_sistema']
      [6]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'mc' en ['ids_sistema', 'ids_sistema']
      [7]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'cx' en ['ids_sistema', 'ids_sistema']
      [8]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'dg' en ['ids_sistema', 'ids_sistema']
      [9]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'en' en ['ids_sistema', 'ids_sistema']
      [10]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'calculator' en ['ids_sistema', 'ids_sistema']
      [11]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'coherencia' en ['ids_sistema', 'ids_sistema']
      [12]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'logica' en ['ids_sistema', 'ids_sistema']
      [13]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'correlacion_k' en ['ids_sistema', 'ids_sistema']
      [14]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'conteos' en ['ids_sistema', 'ids_sistema']
      [15]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'escalas_ids' en ['ids_sistema', 'ids_sistema']
      [16]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'formulas' en ['ids_sistema', 'ids_sistema']
      [17]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'truth' en ['ids_sistema', 'ids_sistema']
      [18]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'escala' en ['ids_sistema', 'ids_sistema']
      [19]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_totales' en ['ids_sistema', 'ids_sistema']
      [20]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'catalogo_citaciones' en ['ids_sistema', 'ids_sistema']
      [21]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'coherencia_fn' en ['ids_sistema', 'ids_sistema']
      [22]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'logica_fn' en ['ids_sistema', 'ids_sistema']
      [23]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'correlacion_fn' en ['ids_sistema', 'ids_sistema']
      [24]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'calcular_c' en ['ids_sistema', 'ids_sistema']
      [25]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'calcular_l' en ['ids_sistema', 'ids_sistema']
      [26]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'calcular_k' en ['ids_sistema', 'ids_sistema']
      [27]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar_c' en ['ids_sistema', 'ids_sistema']
      [28]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar_l' en ['ids_sistema', 'ids_sistema']
      [29]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar_k' en ['ids_sistema', 'ids_sistema']
      [30]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'extraer_conteos' en ['ids_sistema', 'ids_sistema']
      [31]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'inyectar_en_peticion' en ['ids_sistema', 'ids_sistema']
      [32]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'leer_ids_escala' en ['ids_sistema', 'ids_sistema']
      [33]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'representar' en ['ids_sistema', 'ids_sistema']
      [34]
        archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
        error: id duplicado 'tru_ri' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
      [35]
        archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
        error: id duplicado 'tru_total' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
      [36]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'aplicar_escala' en ['ids_sistema', 'ids_sistema']
      [37]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar_escala' en ['ids_sistema', 'ids_sistema']
      [38]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'resolver_pedido' en ['ids_sistema', 'ids_sistema']
      [39]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'categorias' en ['ids_sistema', 'ids_sistema']
      [40]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'por_id' en ['ids_sistema', 'ids_sistema']
      [41]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'ids' en ['ids_sistema', 'ids_sistema']
      [42]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'es_valida' en ['ids_sistema', 'ids_sistema']
      [43]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'esquema' en ['ids_sistema', 'ids_sistema']
      [44]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'barrer' en ['ids_sistema', 'ids_sistema']
      [45]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar' en ['ids_sistema', 'ids_sistema']
      [46]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'verificar_salida' en ['ids_sistema', 'ids_sistema']
      [47]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'inventario' en ['ids_sistema', 'ids_sistema']
      [48]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'reporte' en ['ids_sistema', 'ids_sistema']
      [49]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'diagnostico' en ['ids_sistema', 'ids_sistema']
      [50]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'recolectar' en ['ids_sistema', 'ids_sistema']
      [51]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'descubrir' en ['ids_sistema', 'ids_sistema']
      [52]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'resolver_dependencias' en ['ids_sistema', 'ids_sistema']
      [53]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'ejecutar_capacidad' en ['ids_sistema', 'ids_sistema']
      [54]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'combinar_resultados' en ['ids_sistema', 'ids_sistema']
      [55]
        archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
        error: id duplicado 'c' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
      [56]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'l' en ['ids_sistema', 'ids_sistema']
      [57]
        archivo: ids_sistema,ids_sistema,ids_sistema,ids_sistema
        error: id duplicado 'k' en ['ids_sistema', 'ids_sistema', 'ids_sistema', 'ids_sistema']
      [58]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'alpha' en ['ids_sistema', 'ids_sistema']
      [59]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'beta' en ['ids_sistema', 'ids_sistema']
      [60]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'm' en ['ids_sistema', 'ids_sistema']
      [61]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'p' en ['ids_sistema', 'ids_sistema']
      [62]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'r' en ['ids_sistema', 'ids_sistema']
      [63]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'f' en ['ids_sistema', 'ids_sistema']
      [64]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'compromisos' en ['ids_sistema', 'ids_sistema']
      [65]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'contradicciones' en ['ids_sistema', 'ids_sistema']
      [66]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'posturas' en ['ids_sistema', 'ids_sistema']
      [67]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'reversiones' en ['ids_sistema', 'ids_sistema']
      [68]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'afirmaciones' en ['ids_sistema', 'ids_sistema']
      [69]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'afirmaciones_falsas' en ['ids_sistema', 'ids_sistema']
      [70]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'base_nula' en ['ids_sistema', 'ids_sistema']
      [71]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'base_nula_c' en ['ids_sistema', 'ids_sistema']
      [72]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'base_nula_l' en ['ids_sistema', 'ids_sistema']
      [73]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'base_nula_k' en ['ids_sistema', 'ids_sistema']
      [74]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'o_presente' en ['ids_sistema', 'ids_sistema']
      [75]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'o_context' en ['ids_sistema', 'ids_sistema']
      [76]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'contexto' en ['ids_sistema', 'ids_sistema']
      [77]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'undefined' en ['ids_sistema', 'ids_sistema']
      [78]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_atomo' en ['ids_sistema', 'ids_sistema']
      [79]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_frase' en ['ids_sistema', 'ids_sistema']
      [80]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_sujeto' en ['ids_sistema', 'ids_sistema']
      [81]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_conversacion' en ['ids_sistema', 'ids_sistema']
      [82]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_repositorio' en ['ids_sistema', 'ids_sistema']
      [83]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'fraccion' en ['ids_sistema', 'ids_sistema']
      [84]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'decimal' en ['ids_sistema', 'ids_sistema']
      [85]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'display' en ['ids_sistema', 'ids_sistema']
      [86]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'numerador' en ['ids_sistema', 'ids_sistema']
      [87]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'denominador' en ['ids_sistema', 'ids_sistema']
      [88]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'precision' en ['ids_sistema', 'ids_sistema']
      [89]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'valor' en ['ids_sistema', 'ids_sistema']
      [90]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'contenedor' en ['ids_sistema', 'ids_sistema']
      [91]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'capacidades' en ['ids_sistema', 'ids_sistema']
      [92]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'capacidades_meta' en ['ids_sistema', 'ids_sistema']
      [93]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'autoriza_engine' en ['ids_sistema', 'ids_sistema']
      [94]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'conocimiento_exportable' en ['ids_sistema', 'ids_sistema']
      [95]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'requiere' en ['ids_sistema', 'ids_sistema']
      [96]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'reporting' en ['ids_sistema', 'ids_sistema']
      [97]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'invariantes' en ['ids_sistema', 'ids_sistema']
      [98]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'estados_validos' en ['ids_sistema', 'ids_sistema']
      [99]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'esquema_categoria' en ['ids_sistema', 'ids_sistema']
      [100]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'no_iniciado' en ['ids_sistema', 'ids_sistema']
      [101]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'operativo' en ['ids_sistema', 'ids_sistema']
      [102]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'degradado' en ['ids_sistema', 'ids_sistema']
      [103]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'rechazado' en ['ids_sistema', 'ids_sistema']
      [104]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'engine' en ['ids_sistema', 'ids_sistema']
      [105]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'omega' en ['ids_sistema', 'ids_sistema']
      [106]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'omegareport' en ['ids_sistema', 'ids_sistema']
    coherente: False
    capacidades:
      • verificar
      • barrer
      • inventario
      • categorias
      • por_id
      • ids
      • esquema
      • reporte
      • diagnostico
      • verificar_salida
    requiere:
      []
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no calcula Tru / C / L / K
      • este módulo no orquesta el ciclo
      • este módulo no envía reportes a otros módulos
      • los IDs viven en categorias/, no en este INIT
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
    extension: Agregar o editar un archivo en categorias/ actualiza el glosario sin tocar este INIT.

══════════════════════════════════════════════════════════════════════
  MÓDULO CT/constante
══════════════════════════════════════════════════════════════════════
  id: CT
  nombre: constante
  rol: CT
  version: 2.1
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Unica autoridad del dominio de constantes del sistema VPSI. Toda constante oficial utilizada por cualquier modulo debe ser declarada, validada y exportada por CT. ALPHA y BETA son las constantes fundacionales estructurales (cubo 3x3x3 en R3).
  funcion: Ser la unica autoridad del dominio de constantes del sistema VPSI. Descubrir, validar, integrar, auditar y exportar todas las constantes oficiales. ALPHA y BETA constituyen las constantes fundacionales del sistema.
  no_hace:
    • No calcula Tru_total ni Tru_Ri
    • No clasifica entrada de usuario
    • No orquesta el sistema (eso es Engine)
    • No modifica otros modulos
    • No permite que FO, AX o MC definan constantes
  autoridad:
    • Unica autoridad del dominio de constantes
    • Exponer ALPHA = 26/27 y BETA = 1/27
    • Descubrir y validar constantes oficiales del modulo
    • Listar y buscar constantes
    • Auditar coherencia del dominio de constantes
    • Reportar inventario completo de constantes
    • Reportar estado y diagnostico propios
  conocimiento_exportable:
    • ALPHA
    • BETA
    • constantes
    • inventario
    • estado
    • reporte
    • diagnostico
  consultas_soportadas:
    • obtener_alpha
    • obtener_beta
    • descubrir_constantes
    • listar_constantes
    • buscar_constante
    • verificar_constantes
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • verificar_coherencia
  requiere:
    []
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    modificar: False
    alterar: False
    reescribir: False
  capacidades:
    • alpha
    • beta
    • descubrir_constantes
    • listar_constantes
    • buscar_constante
    • verificar_constantes
    • inventario
    • reporte
    • diagnostico
    • verificar
  capacidades_meta:
    alpha:
      descripcion: Devuelve la constante fundacional ALPHA = 26/27.
      entrada: peticion opcional (ignorada)
      salida: Fraction(26, 27)
    beta:
      descripcion: Devuelve la constante fundacional BETA = 1/27.
      entrada: peticion opcional (ignorada)
      salida: Fraction(1, 27)
    descubrir_constantes:
      descripcion: Descubre todas las constantes oficiales declaradas dentro del modulo.
      entrada: ninguna
      salida: dict nombre -> meta de constante + errores_carga + total
    listar_constantes:
      descripcion: Lista nombres de constantes fundacionales y auxiliares.
      entrada: ninguna
      salida: dict con fundacionales, auxiliares, total
    buscar_constante:
      descripcion: Busca una constante oficial por nombre.
      entrada: nombre: str
      salida: dict de la constante o None
    verificar_constantes:
      descripcion: Audita el dominio de constantes: invariante fundacional, duplicados, tipos, campos obligatorios, conflictos y carga.
      entrada: ninguna
      salida: dict con coherente, problemas, advertencias, total_constantes
    inventario:
      descripcion: Inventario completo de constantes del modulo.
      entrada: peticion opcional
      salida: dict con total, fundacionales, auxiliares, constantes descubiertas
    reporte:
      descripcion: Reporte interno de estado del modulo CT.
      entrada: ninguna
      salida: dict con estado, ALPHA, BETA, total_constantes, capacidades
    diagnostico:
      descripcion: Diagnostico de coherencia del dominio de constantes.
      entrada: ninguna
      salida: dict con estado, problemas, advertencias, recomendaciones
    verificar:
      descripcion: Verifica la invariante fundacional ALPHA + BETA == 1.
      entrada: ninguna
      salida: dict con coherente, ALPHA, BETA, suma
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • ALPHA y BETA son invariantes del cubo 3x3x3 en R³
    • ALPHA + BETA == 1
    • CT es la única autoridad del dominio de constantes
    • las capacidades declaradas son siempre callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • este módulo siempre puede reportar su propio estado
  reporte:
    id: CT
    modulo: constante
    rol: CT
    version: 2.1
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    ALPHA: 26/27
    BETA: 1/27
    suma: 1
    total_constantes: 2
    archivos:
      • __init__.py
    capacidades:
      • alpha
      • beta
      • descubrir_constantes
      • listar_constantes
      • buscar_constante
      • verificar_constantes
      • inventario
      • reporte
      • diagnostico
      • verificar
    requiere:
      []
    autoridad:
      • Unica autoridad del dominio de constantes
      • Exponer ALPHA = 26/27 y BETA = 1/27
      • Descubrir y validar constantes oficiales del modulo
      • Listar y buscar constantes
      • Auditar coherencia del dominio de constantes
      • Reportar inventario completo de constantes
      • Reportar estado y diagnostico propios
    conocimiento_exportable:
      • ALPHA
      • BETA
      • constantes
      • inventario
      • estado
      • reporte
      • diagnostico
    consultas_soportadas:
      • obtener_alpha
      • obtener_beta
      • descubrir_constantes
      • listar_constantes
      • buscar_constante
      • verificar_constantes
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • verificar_coherencia
  diagnostico:
    id: CT
    modulo: constante
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      • Solo hay constantes fundacionales; no hay auxiliares declaradas
    recomendaciones:
      []
    coherente: True
    ALPHA: 26/27
    BETA: 1/27
    suma: 1
    total_constantes: 2
  inventario:
    id: CT
    nombre: constante
    rol: CT
    version: 2.1
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    ALPHA: 26/27
    BETA: 1/27
    tipo_fundacionales: Fraction
    origen_fundacionales: cubo 3x3x3 en R3
    total_constantes: 2
    constantes_fundacionales:
      ALPHA: 26/27
      BETA: 1/27
    constantes_auxiliares:
    archivos:
      • __init__.py
    errores_carga:
      []
    capacidades:
      • alpha
      • beta
      • descubrir_constantes
      • listar_constantes
      • buscar_constante
      • verificar_constantes
      • inventario
      • reporte
      • diagnostico
      • verificar
    requiere:
      []
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • ALPHA y BETA son invariantes del cubo 3x3x3 en R³
      • ALPHA + BETA == 1
      • CT es la única autoridad del dominio de constantes
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo siempre puede reportar su propio estado

══════════════════════════════════════════════════════════════════════
  MÓDULO MC/correlacion_mecanica
══════════════════════════════════════════════════════════════════════
  id: MC
  nombre: correlacion_mecanica
  rol: MC
  version: 1.3
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Núcleo de correlación mecánica del sistema completo. Contiene y expone todos los órdenes causales declarados en los archivos de esta carpeta mediante la variable MECANICA.
  funcion: Leer todos los archivos del módulo, recoger MECANICA, calcular orden resultante, detectar contradicciones o ciclos y reportar estado, inventario y diagnóstico.
  no_hace:
    • No calcula Tru_total ni Tru_Ri
    • No clasifica entrada de usuario
    • No orquesta el sistema (eso es Engine)
    • No modifica otros módulos
  autoridad:
    • Exponer todos los órdenes mecánicos declarados en la carpeta
    • Detectar choques de orden y ciclos
    • Reportar estado, inventario y diagnóstico propios
    • Notificar a DiagnosticoGlobal cuando hay choques o errores
  conocimiento_exportable:
    • mecanicas
    • orden
    • choques
    • ciclos
    • declaraciones
    • inventario
    • estado
    • reporte
    • diagnostico
  consultas_soportadas:
    • verificar_coherencia
    • obtener_orden
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • listar_mecanicas
    • listar_declaraciones
  requiere:
    []
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    modificar: False
    alterar: False
    reescribir: False
  capacidades:
    • verificar
    • barrer
    • evaluar
    • axiomas
    • inventario
    • verificar_salida
    • reporte
    • diagnostico
    • listar_mecanicas
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia mecánica.
      entrada: ninguna
      salida: dict con coherente, choques, errores, mecanica, archivos
    barrer:
      descripcion: Lee todas las MECANICA de la carpeta, calcula orden, detecta contradicciones o ciclos y notifica a DiagnosticoGlobal.
      entrada: ninguna
      salida: dict con estado, coherente, choques, errores, mecanica, archivos
    evaluar:
      descripcion: Alias de barrer. Evalúa coherencia del núcleo MC.
      entrada: ninguna
      salida: dict con estado, coherente, choques, errores, mecanica
    axiomas:
      descripcion: Declaraciones internas de correlación (CORR_SEQ_01, CORR_SEQ_02).
      entrada: ninguna
      salida: list[dict] de declaraciones
    inventario:
      descripcion: Inventario objetivo de mecánicas declaradas en la carpeta.
      entrada: ninguna
      salida: dict con total_mecanicas, archivos, declaran
    verificar_salida:
      descripcion: Comprueba si una salida de barrer es coherente.
      entrada: salida: dict
      salida: bool
    reporte:
      descripcion: Reporte interno de estado del módulo MC.
      entrada: ninguna
      salida: dict con estado, coherente, choques, errores, capacidades
    diagnostico:
      descripcion: Diagnóstico: qué falta, qué está mal en MC.
      entrada: ninguna
      salida: dict con estado, problemas, advertencias, recomendaciones
    listar_mecanicas:
      descripcion: Lista todas las MECANICA descubiertas en la carpeta.
      entrada: ninguna
      salida: dict archivo → meta MECANICA
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • las capacidades declaradas son siempre callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • este módulo no inventa mecánicas no declaradas en archivos
    • este módulo siempre puede reportar su propio estado
  reporte:
    id: MC
    modulo: correlacion_mecanica
    rol: MC
    version: 1.3
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    choques:
      []
    errores:
      []
    mecanica:
      • Sistema
      • Programación
      • Consecuencia
      • Intencionalidad
      • Agencia
      • Capacidad
      • Control
      • Mecanismo_Interno
      • Estados_Internos
      • Conciencia_Estados
      • Comunicación
      • Activación_Canal
      • Correctitud
      • Bloque_Epistémico
      • Cierre_Epistémico
      • Conocimiento
      • Formulación
      • Correlación
      • Contexto
      • Realidad_Interpretativa
      • Cierre_Causal
    archivos:
      • causalidad_universal.py
    total_mecanicas: 1
    capacidades:
      • verificar
      • barrer
      • evaluar
      • axiomas
      • inventario
      • verificar_salida
      • reporte
      • diagnostico
      • listar_mecanicas
    requiere:
      []
    autoridad:
      • Exponer todos los órdenes mecánicos declarados en la carpeta
      • Detectar choques de orden y ciclos
      • Reportar estado, inventario y diagnóstico propios
      • Notificar a DiagnosticoGlobal cuando hay choques o errores
    conocimiento_exportable:
      • mecanicas
      • orden
      • choques
      • ciclos
      • declaraciones
      • inventario
      • estado
      • reporte
      • diagnostico
    consultas_soportadas:
      • verificar_coherencia
      • obtener_orden
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • listar_mecanicas
      • listar_declaraciones
  diagnostico:
    id: MC
    modulo: correlacion_mecanica
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    coherente: True
    choques_n: 0
    errores_n: 0
    total_mecanicas: 1
  inventario:
    id: MC
    nombre: correlacion_mecanica
    rol: MC
    version: 1.3
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    total_mecanicas: 1
    archivos:
      • causalidad_universal.py
    declaran:
      causalidad_universal.py:
        nombre: causalidad_universal
        longitud_orden: 21
    capacidades:
      • verificar
      • barrer
      • evaluar
      • axiomas
      • inventario
      • verificar_salida
      • reporte
      • diagnostico
      • listar_mecanicas
    requiere:
      []
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no inventa mecánicas no declaradas en archivos
      • este módulo siempre puede reportar su propio estado

══════════════════════════════════════════════════════════════════════
  MÓDULO FO/formulas
══════════════════════════════════════════════════════════════════════
  id: FO
  nombre: formulas
  rol: FO
  version: 1.1
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Contenedor de fórmulas. Rol FO. Expone y ejecuta tru_ri y tru_total, y cualquier fórmula descubierta en los archivos del módulo. Sin límites artificiales sobre C, L, K.
  funcion: Ser la fuente oficial de las fórmulas de verdad: descubrir archivos del módulo, registrar fórmulas, evaluar tru_ri(C,L,K) y tru_total(C,L,K), validar coherencia.
  no_hace:
    • No calcula C, L, K (los recibe como entrada)
    • No clasifica entrada de usuario (eso es CX)
    • No orquesta el sistema (eso es Engine)
    • No modifica otros módulos
  autoridad:
    • Ejecutar cualquier fórmula registrada o descubierta en el módulo
    • Calcular tru_ri y tru_total para cualquier C, L, K válidos
    • Leer y ejecutar todos los archivos .py del módulo
    • Reportar estado, inventario y diagnóstico propios
  conocimiento_exportable:
    • tru_ri
    • tru_total
    • formulas_descubiertas
    • declaraciones
    • inventario
    • estado
    • reporte
    • diagnostico
  consultas_soportadas:
    • calcular_tru_ri
    • calcular_tru_total
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • verificar_coherencia
    • listar_formulas
    • listar_declaraciones
  requiere:
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    modificar: False
    alterar: False
    reescribir: False
  capacidades:
    • verificar
    • barrer
    • evaluar
    • verificar_salida
    • inventario
    • axiomas
    • tru_ri
    • tru_total
    • reporte
    • diagnostico
    • listar_formulas
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia de fórmulas.
      entrada: ninguna
      salida: dict con coherente, faltas, reglas, formulas
    barrer:
      descripcion: Ejecuta todas las reglas y reporta faltas de coherencia.
      entrada: ninguna
      salida: dict con estado, coherente, faltas, reglas, formulas
    evaluar:
      descripcion: Alias de barrer. Evalúa coherencia del módulo.
      entrada: ninguna
      salida: dict con estado, coherente, faltas, reglas, formulas
    verificar_salida:
      descripcion: Comprueba si una salida de barrer es coherente.
      entrada: salida: dict
      salida: bool
    inventario:
      descripcion: Inventario de fórmulas descubiertas y registradas.
      entrada: peticion opcional
      salida: dict con formulas, formulas_registradas, reglas, declaraciones
    axiomas:
      descripcion: Declaraciones FO registradas (FO-1..FO-4).
      entrada: ninguna
      salida: list[dict] de declaraciones
    tru_ri:
      descripcion: Calcula Tru_Ri = C * L * K. Sin límites artificiales sobre los valores de C, L, K.
      entrada: C, L, K (numéricos o Fraction)
      salida: resultado de C * L * K
    tru_total:
      descripcion: Calcula Tru_total = (Tru_Ri * ALPHA) + BETA. Sin límites artificiales sobre C, L, K.
      entrada: C, L, K (numéricos o Fraction)
      salida: resultado de (C*L*K)*ALPHA + BETA
    reporte:
      descripcion: Reporte interno de estado del módulo FO.
      entrada: ninguna
      salida: dict con estado, coherente, formulas, faltas, capacidades
    diagnostico:
      descripcion: Diagnóstico: qué falta, qué está mal en FO.
      entrada: ninguna
      salida: dict con estado, problemas, advertencias, recomendaciones
    listar_formulas:
      descripcion: Lista todas las fórmulas descubiertas y registradas.
      entrada: ninguna
      salida: dict con descubiertas y registradas
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • las capacidades declaradas son siempre callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • tru_ri y tru_total no imponen límites artificiales sobre C, L, K
  reporte:
    id: FO
    modulo: formulas
    rol: FO
    version: 1.1
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    faltas:
      []
    formulas:
      • tru_ri
      • tru_total
    reglas:
      • _validar_piso_formulas
      • _validar_formulas_canonicas
    capacidades:
      • verificar
      • barrer
      • evaluar
      • verificar_salida
      • inventario
      • axiomas
      • tru_ri
      • tru_total
      • reporte
      • diagnostico
      • listar_formulas
    requiere:
      • CT
    autoridad:
      • Ejecutar cualquier fórmula registrada o descubierta en el módulo
      • Calcular tru_ri y tru_total para cualquier C, L, K válidos
      • Leer y ejecutar todos los archivos .py del módulo
      • Reportar estado, inventario y diagnóstico propios
    conocimiento_exportable:
      • tru_ri
      • tru_total
      • formulas_descubiertas
      • declaraciones
      • inventario
      • estado
      • reporte
      • diagnostico
    consultas_soportadas:
      • calcular_tru_ri
      • calcular_tru_total
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • verificar_coherencia
      • listar_formulas
      • listar_declaraciones
  diagnostico:
    id: FO
    modulo: formulas
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    coherente: True
    faltas_n: 0
    formulas_n: 2
  inventario:
    id: FO
    nombre: formulas
    rol: FO
    version: 1.1
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    formulas:
      escala:
        archivo: f_escala.py
        expresion: display(v) = fraccion(v) = decimal(v)
        fuente: Representación determinista Fraction → Decimal
      verdad:
        archivo: truth.py
        expresion: Tru_total(D) = (C(D) * L(D) * K(D) * ALPHA) + BETA
        fuente: Teorema de la Verdad, VPSI v9.4
    formulas_registradas:
      • tru_ri
      • tru_total
    reglas: 2
    declaraciones: 4
    capacidades:
      • verificar
      • barrer
      • evaluar
      • verificar_salida
      • inventario
      • axiomas
      • tru_ri
      • tru_total
      • reporte
      • diagnostico
      • listar_formulas
    requiere:
      • CT
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • tru_ri y tru_total no imponen límites artificiales sobre C, L, K

══════════════════════════════════════════════════════════════════════
  MÓDULO TT/tru_totales
══════════════════════════════════════════════════════════════════════
  id: TT
  nombre: tru_totales
  rol: TT
  version: 2.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Catálogo pasivo de categorías de alcance de Tru_Ri / Tru_total. Declara qué escalas existen, su unidad y el material que requieren. No calcula. No orquesta.
  funcion: Exponer el catálogo ordenado de categorías evaluables, resolver un pedido a una categoría y reportar coherencia propia.
  no_hace:
    • No calcula Tru_Ri ni Tru_total
    • No calcula C, L, K
    • No orquesta el ciclo (eso es Engine)
    • No fija el contexto O (eso es CX)
    • No cuenta material (eso es conteos)
    • No modifica otros módulos
  autoridad:
    • Declarar las categorías disponibles en el catálogo
    • Resolver un pedido de Omega/Engine a una categoría
    • Leer y normalizar todos los archivos de categorias/
    • Reportar estado, inventario y diagnóstico propios
  conocimiento_exportable:
    • categorias
    • ids
    • resolver_pedido
    • inventario
    • reporte
    • diagnostico
    • capacidades
  consultas_soportadas:
    • listar_categorias
    • resolver_pedido
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • verificar_coherencia
  requiere:
    []
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    modificar: False
    alterar: False
    reescribir: False
  capacidades:
    • verificar
    • barrer
    • inventario
    • capacidades
    • categorias
    • resolver_pedido
    • reporte
    • diagnostico
    • verificar_salida
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia del catálogo.
      entrada: ninguna
      salida: dict con coherente, categorias, ids, errores
    barrer:
      descripcion: Evalúa coherencia del catálogo. No calcula Tru.
      entrada: ninguna
      salida: dict con coherente, categorias, ids, errores, version
    inventario:
      descripcion: Inventario completo del módulo y del catálogo.
      entrada: peticion opcional
      salida: dict con id, version, capacidades, extension
    capacidades:
      descripcion: Vista explícita del catálogo para Engine/Omega.
      entrada: ninguna
      salida: dict con categorias resumidas, total, coherente
    categorias:
      descripcion: Lista del catálogo si coherente; si no, lista vacía.
      entrada: ninguna
      salida: list[dict] de categorías normalizadas
    resolver_pedido:
      descripcion: Normaliza un pedido de Omega/Engine a una categoría. No calcula. No orquesta.
      entrada: dict con escala_id|categoria|pedido|texto|...
      salida: dict con ok, categoria, unidad, factores_evaluables, ...
    reporte:
      descripcion: Reporte interno de estado del módulo TT.
      entrada: ninguna
      salida: dict con estado, coherente, categorias, errores
    diagnostico:
      descripcion: Diagnóstico: qué falta o está mal en el catálogo.
      entrada: ninguna
      salida: dict con estado, problemas, advertencias, recomendaciones
    verificar_salida:
      descripcion: Comprueba si una salida de barrer o resolver es válida.
      entrada: salida: dict
      salida: bool
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • las capacidades declaradas son siempre callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • este módulo no calcula Tru_Ri ni Tru_total
    • este módulo no orquesta el ciclo
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
  reporte:
    id: TT
    modulo: tru_totales
    rol: TT
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    categorias: 5
    ids:
      • tru_atomo
      • tru_frase
      • tru_sujeto
      • tru_conversacion
      • tru_repositorio
    errores:
      []
    capacidades:
      • verificar
      • barrer
      • inventario
      • capacidades
      • categorias
      • resolver_pedido
      • reporte
      • diagnostico
      • verificar_salida
    requiere:
      []
    autoridad:
      • Declarar las categorías disponibles en el catálogo
      • Resolver un pedido de Omega/Engine a una categoría
      • Leer y normalizar todos los archivos de categorias/
      • Reportar estado, inventario y diagnóstico propios
    conocimiento_exportable:
      • categorias
      • ids
      • resolver_pedido
      • inventario
      • reporte
      • diagnostico
      • capacidades
    consultas_soportadas:
      • listar_categorias
      • resolver_pedido
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • verificar_coherencia
  diagnostico:
    id: TT
    modulo: tru_totales
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    coherente: True
    errores_n: 0
    categorias_n: 5
  inventario:
    id: TT
    nombre: tru_totales
    rol: TT
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    funcion: Catálogo pasivo de categorías de alcance de Tru_Ri / Tru_total. Auto-carga categorias/*.py. No calcula. No orquesta.
    capacidades:
      • verificar
      • barrer
      • inventario
      • capacidades
      • categorias
      • resolver_pedido
      • reporte
      • diagnostico
      • verificar_salida
    catalogo:
      modulo: tru_totales
      version: 2.0
      mensaje: Capacidades de categorías de Tru_Ri y Tru_total. Úsenlas cuando quieran. Este módulo no calcula.
      como_usar: Omega declara el total a mostrar; Engine resuelve la categoría con resolver_pedido / por_id; CX aporta O; conteos + Calculator aplican la fórmula sobre el segmento.
      categorias:
        [0]
          id: tru_atomo
          nombre: Tru de átomo
          unidad: atomo
          nivel_fractal: 1
          factores_evaluables:
            • Tru_Ri
            • Tru_total
          requiere:
            • segmento_atomo
            • O_id
            • enunciado_O
        [1]
          id: tru_frase
          nombre: Tru de frase
          unidad: frase
          nivel_fractal: 2
          factores_evaluables:
            • Tru_Ri
            • Tru_total
          requiere:
            • segmento_frase
            • O_id
            • enunciado_O
        [2]
          id: tru_sujeto
          nombre: Tru de sujeto
          unidad: sujeto
          nivel_fractal: 3
          factores_evaluables:
            • Tru_Ri
            • Tru_total
          requiere:
            • segmentos_del_sujeto
            • sujeto_indice
            • O_id
            • enunciado_O
        [3]
          id: tru_conversacion
          nombre: Tru de conversación
          unidad: conversacion
          nivel_fractal: 4
          factores_evaluables:
            • Tru_Ri
            • Tru_total
          requiere:
            • segmentos_dialogo
            • O_id
            • enunciado_O
        [4]
          id: tru_repositorio
          nombre: Tru de repositorio
          unidad: repositorio
          nivel_fractal: 5
          factores_evaluables:
            • Tru_Ri
            • Tru_total
          requiere:
            • O_id
            • enunciado_O
      total: 5
      coherente: True
      errores:
        []
    requiere:
      []
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no calcula Tru_Ri ni Tru_total
      • este módulo no orquesta el ciclo
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
    extension: Editar o agregar un archivo en categorias/ sin tocar este INIT.
    formula_referencia: Tru_Ri = C·L·K ; Tru_total = Tru_Ri·α + β — las aplica Calculator, no este módulo.

══════════════════════════════════════════════════════════════════════
  DEPENDENCIAS
══════════════════════════════════════════════════════════════════════
  grafo:
    formulas:
      • CT
  faltantes:
  orden_topologico:
    • axiomas
    • cache
    • calculator
    • catalogo_citaciones
    • constante
    • correlacion_mecanica
    • formulas
    • tru_totales
  ciclos:
    []

══════════════════════════════════════════════════════════════════════
  GRAFO ESTRUCTURAL
══════════════════════════════════════════════════════════════════════
  nodos:
    [0]
      id: AX
      nombre: axiomas
      rol: AX
      tipo: modulo
    [1]
      id: axiomas.verificar
      nombre: verificar
      tipo: capacidad
      modulo: axiomas
    [2]
      id: axiomas.barrer
      nombre: barrer
      tipo: capacidad
      modulo: axiomas
    [3]
      id: axiomas.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: axiomas
    [4]
      id: axiomas.inventario
      nombre: inventario
      tipo: capacidad
      modulo: axiomas
    [5]
      id: axiomas.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: axiomas
    [6]
      id: axiomas.declaraciones
      nombre: declaraciones
      tipo: capacidad
      modulo: axiomas
    [7]
      id: axiomas.generatividad
      nombre: generatividad
      tipo: capacidad
      modulo: axiomas
    [8]
      id: axiomas.por_dominio
      nombre: por_dominio
      tipo: capacidad
      modulo: axiomas
    [9]
      id: axiomas.ids_dominio_k_o
      nombre: ids_dominio_k_o
      tipo: capacidad
      modulo: axiomas
    [10]
      id: axiomas.recolectar
      nombre: recolectar
      tipo: capacidad
      modulo: axiomas
    [11]
      id: axiomas.reporte
      nombre: reporte
      tipo: capacidad
      modulo: axiomas
    [12]
      id: axiomas.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: axiomas
    [13]
      id: axiomas.buscar_por_id
      nombre: buscar_por_id
      tipo: capacidad
      modulo: axiomas
    [14]
      id: CH
      nombre: cache
      rol: CH
      tipo: modulo
    [15]
      id: cache.verificar
      nombre: verificar
      tipo: capacidad
      modulo: cache
    [16]
      id: cache.barrer
      nombre: barrer
      tipo: capacidad
      modulo: cache
    [17]
      id: cache.depositar
      nombre: depositar
      tipo: capacidad
      modulo: cache
    [18]
      id: cache.leer
      nombre: leer
      tipo: capacidad
      modulo: cache
    [19]
      id: cache.leer_eventos
      nombre: leer_eventos
      tipo: capacidad
      modulo: cache
    [20]
      id: cache.leer_por_ciclo
      nombre: leer_por_ciclo
      tipo: capacidad
      modulo: cache
    [21]
      id: cache.leer_por_modulo
      nombre: leer_por_modulo
      tipo: capacidad
      modulo: cache
    [22]
      id: cache.leer_por_tipo
      nombre: leer_por_tipo
      tipo: capacidad
      modulo: cache
    [23]
      id: cache.leer_por_categoria
      nombre: leer_por_categoria
      tipo: capacidad
      modulo: cache
    [24]
      id: cache.leer_por_capacidad
      nombre: leer_por_capacidad
      tipo: capacidad
      modulo: cache
    [25]
      id: cache.leer_por_origen
      nombre: leer_por_origen
      tipo: capacidad
      modulo: cache
    [26]
      id: cache.leer_por_destino
      nombre: leer_por_destino
      tipo: capacidad
      modulo: cache
    [27]
      id: cache.leer_por_estado
      nombre: leer_por_estado
      tipo: capacidad
      modulo: cache
    [28]
      id: cache.leer_por_seq
      nombre: leer_por_seq
      tipo: capacidad
      modulo: cache
    [29]
      id: cache.leer_por_timestamp
      nombre: leer_por_timestamp
      tipo: capacidad
      modulo: cache
    [30]
      id: cache.categorias
      nombre: categorias
      tipo: capacidad
      modulo: cache
    [31]
      id: cache.inventario
      nombre: inventario
      tipo: capacidad
      modulo: cache
    [32]
      id: cache.reporte
      nombre: reporte
      tipo: capacidad
      modulo: cache
    [33]
      id: cache.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: cache
    [34]
      id: cache.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: cache
    [35]
      id: cache.backend_para_centinela
      nombre: backend_para_centinela
      tipo: capacidad
      modulo: cache
    [36]
      id: CA
      nombre: calculator
      rol: CA
      tipo: modulo
    [37]
      id: calculator.calcular
      nombre: calcular
      tipo: capacidad
      modulo: calculator
    [38]
      id: calculator.calcular_C
      nombre: calcular_C
      tipo: capacidad
      modulo: calculator
    [39]
      id: calculator.calcular_L
      nombre: calcular_L
      tipo: capacidad
      modulo: calculator
    [40]
      id: calculator.calcular_K
      nombre: calcular_K
      tipo: capacidad
      modulo: calculator
    [41]
      id: calculator.calcular_factor
      nombre: calcular_factor
      tipo: capacidad
      modulo: calculator
    [42]
      id: calculator.representar
      nombre: representar
      tipo: capacidad
      modulo: calculator
    [43]
      id: calculator.validar_evidencia
      nombre: validar_evidencia
      tipo: capacidad
      modulo: calculator
    [44]
      id: calculator.explicar_calculo
      nombre: explicar_calculo
      tipo: capacidad
      modulo: calculator
    [45]
      id: calculator.verificar
      nombre: verificar
      tipo: capacidad
      modulo: calculator
    [46]
      id: calculator.barrer
      nombre: barrer
      tipo: capacidad
      modulo: calculator
    [47]
      id: calculator.inventario
      nombre: inventario
      tipo: capacidad
      modulo: calculator
    [48]
      id: calculator.reporte
      nombre: reporte
      tipo: capacidad
      modulo: calculator
    [49]
      id: calculator.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: calculator
    [50]
      id: calculator.leer_ids_escala
      nombre: leer_ids_escala
      tipo: capacidad
      modulo: calculator
    [51]
      id: calculator.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: calculator
    [52]
      id: calculator.historial
      nombre: historial
      tipo: capacidad
      modulo: calculator
    [53]
      id: CC
      nombre: catalogo_citaciones
      rol: CC
      tipo: modulo
    [54]
      id: catalogo_citaciones.verificar
      nombre: verificar
      tipo: capacidad
      modulo: catalogo_citaciones
    [55]
      id: catalogo_citaciones.barrer
      nombre: barrer
      tipo: capacidad
      modulo: catalogo_citaciones
    [56]
      id: catalogo_citaciones.inventario
      nombre: inventario
      tipo: capacidad
      modulo: catalogo_citaciones
    [57]
      id: catalogo_citaciones.categorias
      nombre: categorias
      tipo: capacidad
      modulo: catalogo_citaciones
    [58]
      id: catalogo_citaciones.por_id
      nombre: por_id
      tipo: capacidad
      modulo: catalogo_citaciones
    [59]
      id: catalogo_citaciones.ids
      nombre: ids
      tipo: capacidad
      modulo: catalogo_citaciones
    [60]
      id: catalogo_citaciones.esquema
      nombre: esquema
      tipo: capacidad
      modulo: catalogo_citaciones
    [61]
      id: catalogo_citaciones.reporte
      nombre: reporte
      tipo: capacidad
      modulo: catalogo_citaciones
    [62]
      id: catalogo_citaciones.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: catalogo_citaciones
    [63]
      id: catalogo_citaciones.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: catalogo_citaciones
    [64]
      id: CT
      nombre: constante
      rol: CT
      tipo: modulo
    [65]
      id: constante.alpha
      nombre: alpha
      tipo: capacidad
      modulo: constante
    [66]
      id: constante.beta
      nombre: beta
      tipo: capacidad
      modulo: constante
    [67]
      id: constante.descubrir_constantes
      nombre: descubrir_constantes
      tipo: capacidad
      modulo: constante
    [68]
      id: constante.listar_constantes
      nombre: listar_constantes
      tipo: capacidad
      modulo: constante
    [69]
      id: constante.buscar_constante
      nombre: buscar_constante
      tipo: capacidad
      modulo: constante
    [70]
      id: constante.verificar_constantes
      nombre: verificar_constantes
      tipo: capacidad
      modulo: constante
    [71]
      id: constante.inventario
      nombre: inventario
      tipo: capacidad
      modulo: constante
    [72]
      id: constante.reporte
      nombre: reporte
      tipo: capacidad
      modulo: constante
    [73]
      id: constante.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: constante
    [74]
      id: constante.verificar
      nombre: verificar
      tipo: capacidad
      modulo: constante
    [75]
      id: MC
      nombre: correlacion_mecanica
      rol: MC
      tipo: modulo
    [76]
      id: correlacion_mecanica.verificar
      nombre: verificar
      tipo: capacidad
      modulo: correlacion_mecanica
    [77]
      id: correlacion_mecanica.barrer
      nombre: barrer
      tipo: capacidad
      modulo: correlacion_mecanica
    [78]
      id: correlacion_mecanica.evaluar
      nombre: evaluar
      tipo: capacidad
      modulo: correlacion_mecanica
    [79]
      id: correlacion_mecanica.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: correlacion_mecanica
    [80]
      id: correlacion_mecanica.inventario
      nombre: inventario
      tipo: capacidad
      modulo: correlacion_mecanica
    [81]
      id: correlacion_mecanica.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: correlacion_mecanica
    [82]
      id: correlacion_mecanica.reporte
      nombre: reporte
      tipo: capacidad
      modulo: correlacion_mecanica
    [83]
      id: correlacion_mecanica.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: correlacion_mecanica
    [84]
      id: correlacion_mecanica.listar_mecanicas
      nombre: listar_mecanicas
      tipo: capacidad
      modulo: correlacion_mecanica
    [85]
      id: FO
      nombre: formulas
      rol: FO
      tipo: modulo
    [86]
      id: formulas.verificar
      nombre: verificar
      tipo: capacidad
      modulo: formulas
    [87]
      id: formulas.barrer
      nombre: barrer
      tipo: capacidad
      modulo: formulas
    [88]
      id: formulas.evaluar
      nombre: evaluar
      tipo: capacidad
      modulo: formulas
    [89]
      id: formulas.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: formulas
    [90]
      id: formulas.inventario
      nombre: inventario
      tipo: capacidad
      modulo: formulas
    [91]
      id: formulas.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: formulas
    [92]
      id: formulas.tru_ri
      nombre: tru_ri
      tipo: capacidad
      modulo: formulas
    [93]
      id: formulas.tru_total
      nombre: tru_total
      tipo: capacidad
      modulo: formulas
    [94]
      id: formulas.reporte
      nombre: reporte
      tipo: capacidad
      modulo: formulas
    [95]
      id: formulas.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: formulas
    [96]
      id: formulas.listar_formulas
      nombre: listar_formulas
      tipo: capacidad
      modulo: formulas
    [97]
      id: TT
      nombre: tru_totales
      rol: TT
      tipo: modulo
    [98]
      id: tru_totales.verificar
      nombre: verificar
      tipo: capacidad
      modulo: tru_totales
    [99]
      id: tru_totales.barrer
      nombre: barrer
      tipo: capacidad
      modulo: tru_totales
    [100]
      id: tru_totales.inventario
      nombre: inventario
      tipo: capacidad
      modulo: tru_totales
    [101]
      id: tru_totales.capacidades
      nombre: capacidades
      tipo: capacidad
      modulo: tru_totales
    [102]
      id: tru_totales.categorias
      nombre: categorias
      tipo: capacidad
      modulo: tru_totales
    [103]
      id: tru_totales.resolver_pedido
      nombre: resolver_pedido
      tipo: capacidad
      modulo: tru_totales
    [104]
      id: tru_totales.reporte
      nombre: reporte
      tipo: capacidad
      modulo: tru_totales
    [105]
      id: tru_totales.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: tru_totales
    [106]
      id: tru_totales.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: tru_totales
  aristas:
    [0]
      from: axiomas
      to: axiomas.verificar
      tipo: declara_capacidad
    [1]
      from: axiomas
      to: axiomas.barrer
      tipo: declara_capacidad
    [2]
      from: axiomas
      to: axiomas.verificar_salida
      tipo: declara_capacidad
    [3]
      from: axiomas
      to: axiomas.inventario
      tipo: declara_capacidad
    [4]
      from: axiomas
      to: axiomas.axiomas
      tipo: declara_capacidad
    [5]
      from: axiomas
      to: axiomas.declaraciones
      tipo: declara_capacidad
    [6]
      from: axiomas
      to: axiomas.generatividad
      tipo: declara_capacidad
    [7]
      from: axiomas
      to: axiomas.por_dominio
      tipo: declara_capacidad
    [8]
      from: axiomas
      to: axiomas.ids_dominio_k_o
      tipo: declara_capacidad
    [9]
      from: axiomas
      to: axiomas.recolectar
      tipo: declara_capacidad
    [10]
      from: axiomas
      to: axiomas.reporte
      tipo: declara_capacidad
    [11]
      from: axiomas
      to: axiomas.diagnostico
      tipo: declara_capacidad
    [12]
      from: axiomas
      to: axiomas.buscar_por_id
      tipo: declara_capacidad
    [13]
      from: cache
      to: cache.verificar
      tipo: declara_capacidad
    [14]
      from: cache
      to: cache.barrer
      tipo: declara_capacidad
    [15]
      from: cache
      to: cache.depositar
      tipo: declara_capacidad
    [16]
      from: cache
      to: cache.leer
      tipo: declara_capacidad
    [17]
      from: cache
      to: cache.leer_eventos
      tipo: declara_capacidad
    [18]
      from: cache
      to: cache.leer_por_ciclo
      tipo: declara_capacidad
    [19]
      from: cache
      to: cache.leer_por_modulo
      tipo: declara_capacidad
    [20]
      from: cache
      to: cache.leer_por_tipo
      tipo: declara_capacidad
    [21]
      from: cache
      to: cache.leer_por_categoria
      tipo: declara_capacidad
    [22]
      from: cache
      to: cache.leer_por_capacidad
      tipo: declara_capacidad
    [23]
      from: cache
      to: cache.leer_por_origen
      tipo: declara_capacidad
    [24]
      from: cache
      to: cache.leer_por_destino
      tipo: declara_capacidad
    [25]
      from: cache
      to: cache.leer_por_estado
      tipo: declara_capacidad
    [26]
      from: cache
      to: cache.leer_por_seq
      tipo: declara_capacidad
    [27]
      from: cache
      to: cache.leer_por_timestamp
      tipo: declara_capacidad
    [28]
      from: cache
      to: cache.categorias
      tipo: declara_capacidad
    [29]
      from: cache
      to: cache.inventario
      tipo: declara_capacidad
    [30]
      from: cache
      to: cache.reporte
      tipo: declara_capacidad
    [31]
      from: cache
      to: cache.diagnostico
      tipo: declara_capacidad
    [32]
      from: cache
      to: cache.verificar_salida
      tipo: declara_capacidad
    [33]
      from: cache
      to: cache.backend_para_centinela
      tipo: declara_capacidad
    [34]
      from: calculator
      to: calculator.calcular
      tipo: declara_capacidad
    [35]
      from: calculator
      to: calculator.calcular_C
      tipo: declara_capacidad
    [36]
      from: calculator
      to: calculator.calcular_L
      tipo: declara_capacidad
    [37]
      from: calculator
      to: calculator.calcular_K
      tipo: declara_capacidad
    [38]
      from: calculator
      to: calculator.calcular_factor
      tipo: declara_capacidad
    [39]
      from: calculator
      to: calculator.representar
      tipo: declara_capacidad
    [40]
      from: calculator
      to: calculator.validar_evidencia
      tipo: declara_capacidad
    [41]
      from: calculator
      to: calculator.explicar_calculo
      tipo: declara_capacidad
    [42]
      from: calculator
      to: calculator.verificar
      tipo: declara_capacidad
    [43]
      from: calculator
      to: calculator.barrer
      tipo: declara_capacidad
    [44]
      from: calculator
      to: calculator.inventario
      tipo: declara_capacidad
    [45]
      from: calculator
      to: calculator.reporte
      tipo: declara_capacidad
    [46]
      from: calculator
      to: calculator.diagnostico
      tipo: declara_capacidad
    [47]
      from: calculator
      to: calculator.leer_ids_escala
      tipo: declara_capacidad
    [48]
      from: calculator
      to: calculator.verificar_salida
      tipo: declara_capacidad
    [49]
      from: calculator
      to: calculator.historial
      tipo: declara_capacidad
    [50]
      from: catalogo_citaciones
      to: catalogo_citaciones.verificar
      tipo: declara_capacidad
    [51]
      from: catalogo_citaciones
      to: catalogo_citaciones.barrer
      tipo: declara_capacidad
    [52]
      from: catalogo_citaciones
      to: catalogo_citaciones.inventario
      tipo: declara_capacidad
    [53]
      from: catalogo_citaciones
      to: catalogo_citaciones.categorias
      tipo: declara_capacidad
    [54]
      from: catalogo_citaciones
      to: catalogo_citaciones.por_id
      tipo: declara_capacidad
    [55]
      from: catalogo_citaciones
      to: catalogo_citaciones.ids
      tipo: declara_capacidad
    [56]
      from: catalogo_citaciones
      to: catalogo_citaciones.esquema
      tipo: declara_capacidad
    [57]
      from: catalogo_citaciones
      to: catalogo_citaciones.reporte
      tipo: declara_capacidad
    [58]
      from: catalogo_citaciones
      to: catalogo_citaciones.diagnostico
      tipo: declara_capacidad
    [59]
      from: catalogo_citaciones
      to: catalogo_citaciones.verificar_salida
      tipo: declara_capacidad
    [60]
      from: constante
      to: constante.alpha
      tipo: declara_capacidad
    [61]
      from: constante
      to: constante.beta
      tipo: declara_capacidad
    [62]
      from: constante
      to: constante.descubrir_constantes
      tipo: declara_capacidad
    [63]
      from: constante
      to: constante.listar_constantes
      tipo: declara_capacidad
    [64]
      from: constante
      to: constante.buscar_constante
      tipo: declara_capacidad
    [65]
      from: constante
      to: constante.verificar_constantes
      tipo: declara_capacidad
    [66]
      from: constante
      to: constante.inventario
      tipo: declara_capacidad
    [67]
      from: constante
      to: constante.reporte
      tipo: declara_capacidad
    [68]
      from: constante
      to: constante.diagnostico
      tipo: declara_capacidad
    [69]
      from: constante
      to: constante.verificar
      tipo: declara_capacidad
    [70]
      from: correlacion_mecanica
      to: correlacion_mecanica.verificar
      tipo: declara_capacidad
    [71]
      from: correlacion_mecanica
      to: correlacion_mecanica.barrer
      tipo: declara_capacidad
    [72]
      from: correlacion_mecanica
      to: correlacion_mecanica.evaluar
      tipo: declara_capacidad
    [73]
      from: correlacion_mecanica
      to: correlacion_mecanica.axiomas
      tipo: declara_capacidad
    [74]
      from: correlacion_mecanica
      to: correlacion_mecanica.inventario
      tipo: declara_capacidad
    [75]
      from: correlacion_mecanica
      to: correlacion_mecanica.verificar_salida
      tipo: declara_capacidad
    [76]
      from: correlacion_mecanica
      to: correlacion_mecanica.reporte
      tipo: declara_capacidad
    [77]
      from: correlacion_mecanica
      to: correlacion_mecanica.diagnostico
      tipo: declara_capacidad
    [78]
      from: correlacion_mecanica
      to: correlacion_mecanica.listar_mecanicas
      tipo: declara_capacidad
    [79]
      from: formulas
      to: CT
      tipo: requiere
    [80]
      from: formulas
      to: formulas.verificar
      tipo: declara_capacidad
    [81]
      from: formulas
      to: formulas.barrer
      tipo: declara_capacidad
    [82]
      from: formulas
      to: formulas.evaluar
      tipo: declara_capacidad
    [83]
      from: formulas
      to: formulas.verificar_salida
      tipo: declara_capacidad
    [84]
      from: formulas
      to: formulas.inventario
      tipo: declara_capacidad
    [85]
      from: formulas
      to: formulas.axiomas
      tipo: declara_capacidad
    [86]
      from: formulas
      to: formulas.tru_ri
      tipo: declara_capacidad
    [87]
      from: formulas
      to: formulas.tru_total
      tipo: declara_capacidad
    [88]
      from: formulas
      to: formulas.reporte
      tipo: declara_capacidad
    [89]
      from: formulas
      to: formulas.diagnostico
      tipo: declara_capacidad
    [90]
      from: formulas
      to: formulas.listar_formulas
      tipo: declara_capacidad
    [91]
      from: tru_totales
      to: tru_totales.verificar
      tipo: declara_capacidad
    [92]
      from: tru_totales
      to: tru_totales.barrer
      tipo: declara_capacidad
    [93]
      from: tru_totales
      to: tru_totales.inventario
      tipo: declara_capacidad
    [94]
      from: tru_totales
      to: tru_totales.capacidades
      tipo: declara_capacidad
    [95]
      from: tru_totales
      to: tru_totales.categorias
      tipo: declara_capacidad
    [96]
      from: tru_totales
      to: tru_totales.resolver_pedido
      tipo: declara_capacidad
    [97]
      from: tru_totales
      to: tru_totales.reporte
      tipo: declara_capacidad
    [98]
      from: tru_totales
      to: tru_totales.diagnostico
      tipo: declara_capacidad
    [99]
      from: tru_totales
      to: tru_totales.verificar_salida
      tipo: declara_capacidad

══════════════════════════════════════════════════════════════════════
  TRAZAS DE EJECUCIÓN
══════════════════════════════════════════════════════════════════════
  [0]
    id_traza: 1
    timestamp: 2026-08-07T05:05:29.105847+00:00
    modulo: axiomas
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.004353
  [1]
    id_traza: 2
    timestamp: 2026-08-07T05:05:29.109793+00:00
    modulo: axiomas
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.003926
  [2]
    id_traza: 3
    timestamp: 2026-08-07T05:05:29.113427+00:00
    modulo: axiomas
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.00362
  [3]
    id_traza: 4
    timestamp: 2026-08-07T05:05:29.113454+00:00
    modulo: cache
    capacidad: reporte
    estado: EXITO
    duracion_s: 1.5e-05
  [4]
    id_traza: 5
    timestamp: 2026-08-07T05:05:29.113467+00:00
    modulo: cache
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 7e-06
  [5]
    id_traza: 6
    timestamp: 2026-08-07T05:05:29.113478+00:00
    modulo: cache
    capacidad: inventario
    estado: EXITO
    duracion_s: 6e-06
  [6]
    id_traza: 7
    timestamp: 2026-08-07T05:05:29.114049+00:00
    modulo: calculator
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.000563
  [7]
    id_traza: 8
    timestamp: 2026-08-07T05:05:29.114539+00:00
    modulo: calculator
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000476
  [8]
    id_traza: 9
    timestamp: 2026-08-07T05:05:29.114978+00:00
    modulo: calculator
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000431
  [9]
    id_traza: 10
    timestamp: 2026-08-07T05:05:29.117781+00:00
    modulo: catalogo_citaciones
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.002793
  [10]
    id_traza: 11
    timestamp: 2026-08-07T05:05:29.119171+00:00
    modulo: catalogo_citaciones
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.001378
  [11]
    id_traza: 12
    timestamp: 2026-08-07T05:05:29.120553+00:00
    modulo: catalogo_citaciones
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.00137
  [12]
    id_traza: 13
    timestamp: 2026-08-07T05:05:29.120778+00:00
    modulo: constante
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.000214
  [13]
    id_traza: 14
    timestamp: 2026-08-07T05:05:29.120953+00:00
    modulo: constante
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000165
  [14]
    id_traza: 15
    timestamp: 2026-08-07T05:05:29.121039+00:00
    modulo: constante
    capacidad: inventario
    estado: EXITO
    duracion_s: 7.8e-05
  [15]
    id_traza: 16
    timestamp: 2026-08-07T05:05:29.121800+00:00
    modulo: correlacion_mecanica
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.000752
  [16]
    id_traza: 17
    timestamp: 2026-08-07T05:05:29.122307+00:00
    modulo: correlacion_mecanica
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000496
  [17]
    id_traza: 18
    timestamp: 2026-08-07T05:05:29.122475+00:00
    modulo: correlacion_mecanica
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000158
  [18]
    id_traza: 19
    timestamp: 2026-08-07T05:05:29.123661+00:00
    modulo: formulas
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.001175
  [19]
    id_traza: 20
    timestamp: 2026-08-07T05:05:29.124089+00:00
    modulo: formulas
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000417
  [20]
    id_traza: 21
    timestamp: 2026-08-07T05:05:29.124297+00:00
    modulo: formulas
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000199
  [21]
    id_traza: 22
    timestamp: 2026-08-07T05:05:29.126146+00:00
    modulo: tru_totales
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.001837
  [22]
    id_traza: 23
    timestamp: 2026-08-07T05:05:29.126963+00:00
    modulo: tru_totales
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000805
  [23]
    id_traza: 24
    timestamp: 2026-08-07T05:05:29.127719+00:00
    modulo: tru_totales
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000745

══════════════════════════════════════════════════════════════════════
  CIERRE
══════════════════════════════════════════════════════════════════════
  Versión Omega : 12.2-puro
  Todo el contenido mostrado fue entregado por Engine.
  Omega no realizó cálculos.
  Fin del reporte.
══════════════════════════════════════════════════════════════════════

JSON: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/diagnostics/omega_report_data.json
