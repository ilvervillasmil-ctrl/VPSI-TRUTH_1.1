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
  total_modulos: 6
  timestamp: 2026-08-07T02:56:36.642683+00:00

══════════════════════════════════════════════════════════════════════
  INFORMACIÓN DEL RUN
══════════════════════════════════════════════════════════════════════
  version_engine: 18.3
  esquema_contrato: VPSI-CONTRACT-1.0
  version_contrato_requerida: 1.0
  api_engine: 1.0
  estado_engine: OPERATIVO
  invocador_id: omega_report
  total_modulos: 6
  errores_arranque:
    []
  advertencias:
    []
  trazas_n: 18
  timestamp: 2026-08-07T02:56:36.642655+00:00

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
    declaraciones: 89
    choques: 0
    errores: 0
    cuerpos:
      • VPSI_AX
    por_tipo:
      axioma: 42
      lema: 5
      teorema: 31
      corolario: 11
      definicion: 0
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
    declaraciones: 89
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
    declaraciones: 89
    por_tipo:
      axioma: 42
      lema: 5
      teorema: 31
      corolario: 11
      definicion: 0
    cuerpos:
      • VPSI_AX
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
      • B-Canonical
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
        timestamp_mtime: 2026-08-07T02:56:28.243769+00:00
      coherencia.py:
        archivo: coherencia.py
        sha256: ba9d374bca15dc4b36766d151068fdf9895166a60a4352aa0b2706f1a3714313
        tamano: 6153
        timestamp_mtime: 2026-08-07T02:56:28.244217+00:00
      conteos.py:
        archivo: conteos.py
        sha256: 19c30b65365863ef671d9e03aba20e9096b97033681120c4c9ca49dadf352330
        tamano: 20987
        timestamp_mtime: 2026-08-07T02:56:28.244217+00:00
      correlacion_k.py:
        archivo: correlacion_k.py
        sha256: b1cc60d3cc07db792ad4978ff6b14f810d406a62aeae6f552b1795d6695200ab
        tamano: 5546
        timestamp_mtime: 2026-08-07T02:56:28.244217+00:00
      escalas_ids.py:
        archivo: escalas_ids.py
        sha256: 1db219e396c1a9c1cbfdf29ff92842b2b151907c07c6043a70c46349661ba128
        tamano: 2895
        timestamp_mtime: 2026-08-07T02:56:28.244217+00:00
      logica.py:
        archivo: logica.py
        sha256: 39b805c383a02e670d4fd1158e0c95b8e2e41c2d451c8ca377f497c802c236f1
        tamano: 4803
        timestamp_mtime: 2026-08-07T02:56:28.244217+00:00
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
        timestamp_mtime: 2026-08-07T02:56:28.243769+00:00
      coherencia.py:
        archivo: coherencia.py
        sha256: ba9d374bca15dc4b36766d151068fdf9895166a60a4352aa0b2706f1a3714313
        tamano: 6153
        timestamp_mtime: 2026-08-07T02:56:28.244217+00:00
      conteos.py:
        archivo: conteos.py
        sha256: 19c30b65365863ef671d9e03aba20e9096b97033681120c4c9ca49dadf352330
        tamano: 20987
        timestamp_mtime: 2026-08-07T02:56:28.244217+00:00
      correlacion_k.py:
        archivo: correlacion_k.py
        sha256: b1cc60d3cc07db792ad4978ff6b14f810d406a62aeae6f552b1795d6695200ab
        tamano: 5546
        timestamp_mtime: 2026-08-07T02:56:28.244217+00:00
      escalas_ids.py:
        archivo: escalas_ids.py
        sha256: 1db219e396c1a9c1cbfdf29ff92842b2b151907c07c6043a70c46349661ba128
        tamano: 2895
        timestamp_mtime: 2026-08-07T02:56:28.244217+00:00
      logica.py:
        archivo: logica.py
        sha256: 39b805c383a02e670d4fd1158e0c95b8e2e41c2d451c8ca377f497c802c236f1
        tamano: 4803
        timestamp_mtime: 2026-08-07T02:56:28.244217+00:00
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
    categorias: 4
    ids:
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
    categorias_n: 4
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
        [1]
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
        [2]
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
        [3]
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
      total: 4
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
    • calculator
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
      id: CA
      nombre: calculator
      rol: CA
      tipo: modulo
    [15]
      id: calculator.calcular
      nombre: calcular
      tipo: capacidad
      modulo: calculator
    [16]
      id: calculator.calcular_C
      nombre: calcular_C
      tipo: capacidad
      modulo: calculator
    [17]
      id: calculator.calcular_L
      nombre: calcular_L
      tipo: capacidad
      modulo: calculator
    [18]
      id: calculator.calcular_K
      nombre: calcular_K
      tipo: capacidad
      modulo: calculator
    [19]
      id: calculator.calcular_factor
      nombre: calcular_factor
      tipo: capacidad
      modulo: calculator
    [20]
      id: calculator.representar
      nombre: representar
      tipo: capacidad
      modulo: calculator
    [21]
      id: calculator.validar_evidencia
      nombre: validar_evidencia
      tipo: capacidad
      modulo: calculator
    [22]
      id: calculator.explicar_calculo
      nombre: explicar_calculo
      tipo: capacidad
      modulo: calculator
    [23]
      id: calculator.verificar
      nombre: verificar
      tipo: capacidad
      modulo: calculator
    [24]
      id: calculator.barrer
      nombre: barrer
      tipo: capacidad
      modulo: calculator
    [25]
      id: calculator.inventario
      nombre: inventario
      tipo: capacidad
      modulo: calculator
    [26]
      id: calculator.reporte
      nombre: reporte
      tipo: capacidad
      modulo: calculator
    [27]
      id: calculator.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: calculator
    [28]
      id: calculator.leer_ids_escala
      nombre: leer_ids_escala
      tipo: capacidad
      modulo: calculator
    [29]
      id: calculator.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: calculator
    [30]
      id: calculator.historial
      nombre: historial
      tipo: capacidad
      modulo: calculator
    [31]
      id: CT
      nombre: constante
      rol: CT
      tipo: modulo
    [32]
      id: constante.alpha
      nombre: alpha
      tipo: capacidad
      modulo: constante
    [33]
      id: constante.beta
      nombre: beta
      tipo: capacidad
      modulo: constante
    [34]
      id: constante.descubrir_constantes
      nombre: descubrir_constantes
      tipo: capacidad
      modulo: constante
    [35]
      id: constante.listar_constantes
      nombre: listar_constantes
      tipo: capacidad
      modulo: constante
    [36]
      id: constante.buscar_constante
      nombre: buscar_constante
      tipo: capacidad
      modulo: constante
    [37]
      id: constante.verificar_constantes
      nombre: verificar_constantes
      tipo: capacidad
      modulo: constante
    [38]
      id: constante.inventario
      nombre: inventario
      tipo: capacidad
      modulo: constante
    [39]
      id: constante.reporte
      nombre: reporte
      tipo: capacidad
      modulo: constante
    [40]
      id: constante.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: constante
    [41]
      id: constante.verificar
      nombre: verificar
      tipo: capacidad
      modulo: constante
    [42]
      id: MC
      nombre: correlacion_mecanica
      rol: MC
      tipo: modulo
    [43]
      id: correlacion_mecanica.verificar
      nombre: verificar
      tipo: capacidad
      modulo: correlacion_mecanica
    [44]
      id: correlacion_mecanica.barrer
      nombre: barrer
      tipo: capacidad
      modulo: correlacion_mecanica
    [45]
      id: correlacion_mecanica.evaluar
      nombre: evaluar
      tipo: capacidad
      modulo: correlacion_mecanica
    [46]
      id: correlacion_mecanica.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: correlacion_mecanica
    [47]
      id: correlacion_mecanica.inventario
      nombre: inventario
      tipo: capacidad
      modulo: correlacion_mecanica
    [48]
      id: correlacion_mecanica.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: correlacion_mecanica
    [49]
      id: correlacion_mecanica.reporte
      nombre: reporte
      tipo: capacidad
      modulo: correlacion_mecanica
    [50]
      id: correlacion_mecanica.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: correlacion_mecanica
    [51]
      id: correlacion_mecanica.listar_mecanicas
      nombre: listar_mecanicas
      tipo: capacidad
      modulo: correlacion_mecanica
    [52]
      id: FO
      nombre: formulas
      rol: FO
      tipo: modulo
    [53]
      id: formulas.verificar
      nombre: verificar
      tipo: capacidad
      modulo: formulas
    [54]
      id: formulas.barrer
      nombre: barrer
      tipo: capacidad
      modulo: formulas
    [55]
      id: formulas.evaluar
      nombre: evaluar
      tipo: capacidad
      modulo: formulas
    [56]
      id: formulas.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: formulas
    [57]
      id: formulas.inventario
      nombre: inventario
      tipo: capacidad
      modulo: formulas
    [58]
      id: formulas.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: formulas
    [59]
      id: formulas.tru_ri
      nombre: tru_ri
      tipo: capacidad
      modulo: formulas
    [60]
      id: formulas.tru_total
      nombre: tru_total
      tipo: capacidad
      modulo: formulas
    [61]
      id: formulas.reporte
      nombre: reporte
      tipo: capacidad
      modulo: formulas
    [62]
      id: formulas.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: formulas
    [63]
      id: formulas.listar_formulas
      nombre: listar_formulas
      tipo: capacidad
      modulo: formulas
    [64]
      id: TT
      nombre: tru_totales
      rol: TT
      tipo: modulo
    [65]
      id: tru_totales.verificar
      nombre: verificar
      tipo: capacidad
      modulo: tru_totales
    [66]
      id: tru_totales.barrer
      nombre: barrer
      tipo: capacidad
      modulo: tru_totales
    [67]
      id: tru_totales.inventario
      nombre: inventario
      tipo: capacidad
      modulo: tru_totales
    [68]
      id: tru_totales.capacidades
      nombre: capacidades
      tipo: capacidad
      modulo: tru_totales
    [69]
      id: tru_totales.categorias
      nombre: categorias
      tipo: capacidad
      modulo: tru_totales
    [70]
      id: tru_totales.resolver_pedido
      nombre: resolver_pedido
      tipo: capacidad
      modulo: tru_totales
    [71]
      id: tru_totales.reporte
      nombre: reporte
      tipo: capacidad
      modulo: tru_totales
    [72]
      id: tru_totales.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: tru_totales
    [73]
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
      from: calculator
      to: calculator.calcular
      tipo: declara_capacidad
    [14]
      from: calculator
      to: calculator.calcular_C
      tipo: declara_capacidad
    [15]
      from: calculator
      to: calculator.calcular_L
      tipo: declara_capacidad
    [16]
      from: calculator
      to: calculator.calcular_K
      tipo: declara_capacidad
    [17]
      from: calculator
      to: calculator.calcular_factor
      tipo: declara_capacidad
    [18]
      from: calculator
      to: calculator.representar
      tipo: declara_capacidad
    [19]
      from: calculator
      to: calculator.validar_evidencia
      tipo: declara_capacidad
    [20]
      from: calculator
      to: calculator.explicar_calculo
      tipo: declara_capacidad
    [21]
      from: calculator
      to: calculator.verificar
      tipo: declara_capacidad
    [22]
      from: calculator
      to: calculator.barrer
      tipo: declara_capacidad
    [23]
      from: calculator
      to: calculator.inventario
      tipo: declara_capacidad
    [24]
      from: calculator
      to: calculator.reporte
      tipo: declara_capacidad
    [25]
      from: calculator
      to: calculator.diagnostico
      tipo: declara_capacidad
    [26]
      from: calculator
      to: calculator.leer_ids_escala
      tipo: declara_capacidad
    [27]
      from: calculator
      to: calculator.verificar_salida
      tipo: declara_capacidad
    [28]
      from: calculator
      to: calculator.historial
      tipo: declara_capacidad
    [29]
      from: constante
      to: constante.alpha
      tipo: declara_capacidad
    [30]
      from: constante
      to: constante.beta
      tipo: declara_capacidad
    [31]
      from: constante
      to: constante.descubrir_constantes
      tipo: declara_capacidad
    [32]
      from: constante
      to: constante.listar_constantes
      tipo: declara_capacidad
    [33]
      from: constante
      to: constante.buscar_constante
      tipo: declara_capacidad
    [34]
      from: constante
      to: constante.verificar_constantes
      tipo: declara_capacidad
    [35]
      from: constante
      to: constante.inventario
      tipo: declara_capacidad
    [36]
      from: constante
      to: constante.reporte
      tipo: declara_capacidad
    [37]
      from: constante
      to: constante.diagnostico
      tipo: declara_capacidad
    [38]
      from: constante
      to: constante.verificar
      tipo: declara_capacidad
    [39]
      from: correlacion_mecanica
      to: correlacion_mecanica.verificar
      tipo: declara_capacidad
    [40]
      from: correlacion_mecanica
      to: correlacion_mecanica.barrer
      tipo: declara_capacidad
    [41]
      from: correlacion_mecanica
      to: correlacion_mecanica.evaluar
      tipo: declara_capacidad
    [42]
      from: correlacion_mecanica
      to: correlacion_mecanica.axiomas
      tipo: declara_capacidad
    [43]
      from: correlacion_mecanica
      to: correlacion_mecanica.inventario
      tipo: declara_capacidad
    [44]
      from: correlacion_mecanica
      to: correlacion_mecanica.verificar_salida
      tipo: declara_capacidad
    [45]
      from: correlacion_mecanica
      to: correlacion_mecanica.reporte
      tipo: declara_capacidad
    [46]
      from: correlacion_mecanica
      to: correlacion_mecanica.diagnostico
      tipo: declara_capacidad
    [47]
      from: correlacion_mecanica
      to: correlacion_mecanica.listar_mecanicas
      tipo: declara_capacidad
    [48]
      from: formulas
      to: CT
      tipo: requiere
    [49]
      from: formulas
      to: formulas.verificar
      tipo: declara_capacidad
    [50]
      from: formulas
      to: formulas.barrer
      tipo: declara_capacidad
    [51]
      from: formulas
      to: formulas.evaluar
      tipo: declara_capacidad
    [52]
      from: formulas
      to: formulas.verificar_salida
      tipo: declara_capacidad
    [53]
      from: formulas
      to: formulas.inventario
      tipo: declara_capacidad
    [54]
      from: formulas
      to: formulas.axiomas
      tipo: declara_capacidad
    [55]
      from: formulas
      to: formulas.tru_ri
      tipo: declara_capacidad
    [56]
      from: formulas
      to: formulas.tru_total
      tipo: declara_capacidad
    [57]
      from: formulas
      to: formulas.reporte
      tipo: declara_capacidad
    [58]
      from: formulas
      to: formulas.diagnostico
      tipo: declara_capacidad
    [59]
      from: formulas
      to: formulas.listar_formulas
      tipo: declara_capacidad
    [60]
      from: tru_totales
      to: tru_totales.verificar
      tipo: declara_capacidad
    [61]
      from: tru_totales
      to: tru_totales.barrer
      tipo: declara_capacidad
    [62]
      from: tru_totales
      to: tru_totales.inventario
      tipo: declara_capacidad
    [63]
      from: tru_totales
      to: tru_totales.capacidades
      tipo: declara_capacidad
    [64]
      from: tru_totales
      to: tru_totales.categorias
      tipo: declara_capacidad
    [65]
      from: tru_totales
      to: tru_totales.resolver_pedido
      tipo: declara_capacidad
    [66]
      from: tru_totales
      to: tru_totales.reporte
      tipo: declara_capacidad
    [67]
      from: tru_totales
      to: tru_totales.diagnostico
      tipo: declara_capacidad
    [68]
      from: tru_totales
      to: tru_totales.verificar_salida
      tipo: declara_capacidad

══════════════════════════════════════════════════════════════════════
  TRAZAS DE EJECUCIÓN
══════════════════════════════════════════════════════════════════════
  [0]
    id_traza: 1
    timestamp: 2026-08-07T02:56:36.631346+00:00
    modulo: axiomas
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.002338
  [1]
    id_traza: 2
    timestamp: 2026-08-07T02:56:36.633273+00:00
    modulo: axiomas
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.001908
  [2]
    id_traza: 3
    timestamp: 2026-08-07T02:56:36.635065+00:00
    modulo: axiomas
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.001778
  [3]
    id_traza: 4
    timestamp: 2026-08-07T02:56:36.635583+00:00
    modulo: calculator
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.000504
  [4]
    id_traza: 5
    timestamp: 2026-08-07T02:56:36.636012+00:00
    modulo: calculator
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.00042
  [5]
    id_traza: 6
    timestamp: 2026-08-07T02:56:36.636397+00:00
    modulo: calculator
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000378
  [6]
    id_traza: 7
    timestamp: 2026-08-07T02:56:36.636501+00:00
    modulo: constante
    capacidad: reporte
    estado: EXITO
    duracion_s: 9.7e-05
  [7]
    id_traza: 8
    timestamp: 2026-08-07T02:56:36.636581+00:00
    modulo: constante
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 6.8e-05
  [8]
    id_traza: 9
    timestamp: 2026-08-07T02:56:36.636636+00:00
    modulo: constante
    capacidad: inventario
    estado: EXITO
    duracion_s: 4.9e-05
  [9]
    id_traza: 10
    timestamp: 2026-08-07T02:56:36.637432+00:00
    modulo: correlacion_mecanica
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.000787
  [10]
    id_traza: 11
    timestamp: 2026-08-07T02:56:36.637968+00:00
    modulo: correlacion_mecanica
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000525
  [11]
    id_traza: 12
    timestamp: 2026-08-07T02:56:36.638107+00:00
    modulo: correlacion_mecanica
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000129
  [12]
    id_traza: 13
    timestamp: 2026-08-07T02:56:36.639380+00:00
    modulo: formulas
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.001263
  [13]
    id_traza: 14
    timestamp: 2026-08-07T02:56:36.639812+00:00
    modulo: formulas
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.00042
  [14]
    id_traza: 15
    timestamp: 2026-08-07T02:56:36.640009+00:00
    modulo: formulas
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000187
  [15]
    id_traza: 16
    timestamp: 2026-08-07T02:56:36.641444+00:00
    modulo: tru_totales
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.001425
  [16]
    id_traza: 17
    timestamp: 2026-08-07T02:56:36.642081+00:00
    modulo: tru_totales
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000626
  [17]
    id_traza: 18
    timestamp: 2026-08-07T02:56:36.642642+00:00
    modulo: tru_totales
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.00055

══════════════════════════════════════════════════════════════════════
  CIERRE
══════════════════════════════════════════════════════════════════════
  Versión Omega : 12.2-puro
  Todo el contenido mostrado fue entregado por Engine.
  Omega no realizó cálculos.
  Fin del reporte.
══════════════════════════════════════════════════════════════════════

JSON: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/diagnostics/omega_report_data.json
