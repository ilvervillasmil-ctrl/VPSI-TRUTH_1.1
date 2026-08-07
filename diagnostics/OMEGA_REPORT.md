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
  total_modulos: 4
  timestamp: 2026-08-07T00:37:38.943881+00:00

══════════════════════════════════════════════════════════════════════
  INFORMACIÓN DEL RUN
══════════════════════════════════════════════════════════════════════
  version_engine: 18.3
  esquema_contrato: VPSI-CONTRACT-1.0
  version_contrato_requerida: 1.0
  api_engine: 1.0
  estado_engine: OPERATIVO
  invocador_id: omega_report
  total_modulos: 4
  errores_arranque:
    []
  advertencias:
    []
  trazas_n: 12
  timestamp: 2026-08-07T00:37:38.943861+00:00

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
    estado: DEGRADADO
    coherente: False
    choques:
      []
    errores:
      • ninguna mecánica declarada en la carpeta
    mecanica:
      []
    archivos:
      []
    total_mecanicas: 0
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
    estado: DEGRADADO
    problemas:
      [0]
        tipo: errores_lectura
        detalle:
          • ninguna mecánica declarada en la carpeta
    advertencias:
      • Ninguna mecánica declarada en la carpeta
    recomendaciones:
      • Revisar archivos MECANICA con errores
      • Agregar archivos .py con variable MECANICA
    coherente: False
    choques_n: 0
    errores_n: 1
    total_mecanicas: 0
  inventario:
    id: MC
    nombre: correlacion_mecanica
    rol: MC
    version: 1.3
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    total_mecanicas: 0
    archivos:
      []
    declaran:
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
  DEPENDENCIAS
══════════════════════════════════════════════════════════════════════
  grafo:
    formulas:
      • CT
  faltantes:
  orden_topologico:
    • axiomas
    • constante
    • correlacion_mecanica
    • formulas
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
      id: CT
      nombre: constante
      rol: CT
      tipo: modulo
    [15]
      id: constante.alpha
      nombre: alpha
      tipo: capacidad
      modulo: constante
    [16]
      id: constante.beta
      nombre: beta
      tipo: capacidad
      modulo: constante
    [17]
      id: constante.descubrir_constantes
      nombre: descubrir_constantes
      tipo: capacidad
      modulo: constante
    [18]
      id: constante.listar_constantes
      nombre: listar_constantes
      tipo: capacidad
      modulo: constante
    [19]
      id: constante.buscar_constante
      nombre: buscar_constante
      tipo: capacidad
      modulo: constante
    [20]
      id: constante.verificar_constantes
      nombre: verificar_constantes
      tipo: capacidad
      modulo: constante
    [21]
      id: constante.inventario
      nombre: inventario
      tipo: capacidad
      modulo: constante
    [22]
      id: constante.reporte
      nombre: reporte
      tipo: capacidad
      modulo: constante
    [23]
      id: constante.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: constante
    [24]
      id: constante.verificar
      nombre: verificar
      tipo: capacidad
      modulo: constante
    [25]
      id: MC
      nombre: correlacion_mecanica
      rol: MC
      tipo: modulo
    [26]
      id: correlacion_mecanica.verificar
      nombre: verificar
      tipo: capacidad
      modulo: correlacion_mecanica
    [27]
      id: correlacion_mecanica.barrer
      nombre: barrer
      tipo: capacidad
      modulo: correlacion_mecanica
    [28]
      id: correlacion_mecanica.evaluar
      nombre: evaluar
      tipo: capacidad
      modulo: correlacion_mecanica
    [29]
      id: correlacion_mecanica.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: correlacion_mecanica
    [30]
      id: correlacion_mecanica.inventario
      nombre: inventario
      tipo: capacidad
      modulo: correlacion_mecanica
    [31]
      id: correlacion_mecanica.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: correlacion_mecanica
    [32]
      id: correlacion_mecanica.reporte
      nombre: reporte
      tipo: capacidad
      modulo: correlacion_mecanica
    [33]
      id: correlacion_mecanica.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: correlacion_mecanica
    [34]
      id: correlacion_mecanica.listar_mecanicas
      nombre: listar_mecanicas
      tipo: capacidad
      modulo: correlacion_mecanica
    [35]
      id: FO
      nombre: formulas
      rol: FO
      tipo: modulo
    [36]
      id: formulas.verificar
      nombre: verificar
      tipo: capacidad
      modulo: formulas
    [37]
      id: formulas.barrer
      nombre: barrer
      tipo: capacidad
      modulo: formulas
    [38]
      id: formulas.evaluar
      nombre: evaluar
      tipo: capacidad
      modulo: formulas
    [39]
      id: formulas.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: formulas
    [40]
      id: formulas.inventario
      nombre: inventario
      tipo: capacidad
      modulo: formulas
    [41]
      id: formulas.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: formulas
    [42]
      id: formulas.tru_ri
      nombre: tru_ri
      tipo: capacidad
      modulo: formulas
    [43]
      id: formulas.tru_total
      nombre: tru_total
      tipo: capacidad
      modulo: formulas
    [44]
      id: formulas.reporte
      nombre: reporte
      tipo: capacidad
      modulo: formulas
    [45]
      id: formulas.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: formulas
    [46]
      id: formulas.listar_formulas
      nombre: listar_formulas
      tipo: capacidad
      modulo: formulas
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
      from: constante
      to: constante.alpha
      tipo: declara_capacidad
    [14]
      from: constante
      to: constante.beta
      tipo: declara_capacidad
    [15]
      from: constante
      to: constante.descubrir_constantes
      tipo: declara_capacidad
    [16]
      from: constante
      to: constante.listar_constantes
      tipo: declara_capacidad
    [17]
      from: constante
      to: constante.buscar_constante
      tipo: declara_capacidad
    [18]
      from: constante
      to: constante.verificar_constantes
      tipo: declara_capacidad
    [19]
      from: constante
      to: constante.inventario
      tipo: declara_capacidad
    [20]
      from: constante
      to: constante.reporte
      tipo: declara_capacidad
    [21]
      from: constante
      to: constante.diagnostico
      tipo: declara_capacidad
    [22]
      from: constante
      to: constante.verificar
      tipo: declara_capacidad
    [23]
      from: correlacion_mecanica
      to: correlacion_mecanica.verificar
      tipo: declara_capacidad
    [24]
      from: correlacion_mecanica
      to: correlacion_mecanica.barrer
      tipo: declara_capacidad
    [25]
      from: correlacion_mecanica
      to: correlacion_mecanica.evaluar
      tipo: declara_capacidad
    [26]
      from: correlacion_mecanica
      to: correlacion_mecanica.axiomas
      tipo: declara_capacidad
    [27]
      from: correlacion_mecanica
      to: correlacion_mecanica.inventario
      tipo: declara_capacidad
    [28]
      from: correlacion_mecanica
      to: correlacion_mecanica.verificar_salida
      tipo: declara_capacidad
    [29]
      from: correlacion_mecanica
      to: correlacion_mecanica.reporte
      tipo: declara_capacidad
    [30]
      from: correlacion_mecanica
      to: correlacion_mecanica.diagnostico
      tipo: declara_capacidad
    [31]
      from: correlacion_mecanica
      to: correlacion_mecanica.listar_mecanicas
      tipo: declara_capacidad
    [32]
      from: formulas
      to: CT
      tipo: requiere
    [33]
      from: formulas
      to: formulas.verificar
      tipo: declara_capacidad
    [34]
      from: formulas
      to: formulas.barrer
      tipo: declara_capacidad
    [35]
      from: formulas
      to: formulas.evaluar
      tipo: declara_capacidad
    [36]
      from: formulas
      to: formulas.verificar_salida
      tipo: declara_capacidad
    [37]
      from: formulas
      to: formulas.inventario
      tipo: declara_capacidad
    [38]
      from: formulas
      to: formulas.axiomas
      tipo: declara_capacidad
    [39]
      from: formulas
      to: formulas.tru_ri
      tipo: declara_capacidad
    [40]
      from: formulas
      to: formulas.tru_total
      tipo: declara_capacidad
    [41]
      from: formulas
      to: formulas.reporte
      tipo: declara_capacidad
    [42]
      from: formulas
      to: formulas.diagnostico
      tipo: declara_capacidad
    [43]
      from: formulas
      to: formulas.listar_formulas
      tipo: declara_capacidad

══════════════════════════════════════════════════════════════════════
  TRAZAS DE EJECUCIÓN
══════════════════════════════════════════════════════════════════════
  [0]
    id_traza: 1
    timestamp: 2026-08-07T00:37:38.938498+00:00
    modulo: axiomas
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.002783
  [1]
    id_traza: 2
    timestamp: 2026-08-07T00:37:38.940776+00:00
    modulo: axiomas
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.002256
  [2]
    id_traza: 3
    timestamp: 2026-08-07T00:37:38.942792+00:00
    modulo: axiomas
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.002002
  [3]
    id_traza: 4
    timestamp: 2026-08-07T00:37:38.942956+00:00
    modulo: constante
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.00015
  [4]
    id_traza: 5
    timestamp: 2026-08-07T00:37:38.943023+00:00
    modulo: constante
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 5.9e-05
  [5]
    id_traza: 6
    timestamp: 2026-08-07T00:37:38.943088+00:00
    modulo: constante
    capacidad: inventario
    estado: EXITO
    duracion_s: 5.1e-05
  [6]
    id_traza: 7
    timestamp: 2026-08-07T00:37:38.943124+00:00
    modulo: correlacion_mecanica
    capacidad: reporte
    estado: EXITO
    duracion_s: 3e-05
  [7]
    id_traza: 8
    timestamp: 2026-08-07T00:37:38.943152+00:00
    modulo: correlacion_mecanica
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 1.7e-05
  [8]
    id_traza: 9
    timestamp: 2026-08-07T00:37:38.943174+00:00
    modulo: correlacion_mecanica
    capacidad: inventario
    estado: EXITO
    duracion_s: 1.6e-05
  [9]
    id_traza: 10
    timestamp: 2026-08-07T00:37:38.943476+00:00
    modulo: formulas
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.000296
  [10]
    id_traza: 11
    timestamp: 2026-08-07T00:37:38.943737+00:00
    modulo: formulas
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000253
  [11]
    id_traza: 12
    timestamp: 2026-08-07T00:37:38.943854+00:00
    modulo: formulas
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000108

══════════════════════════════════════════════════════════════════════
  CIERRE
══════════════════════════════════════════════════════════════════════
  Versión Omega : 12.2-puro
  Todo el contenido mostrado fue entregado por Engine.
  Omega no realizó cálculos.
  Fin del reporte.
══════════════════════════════════════════════════════════════════════

JSON: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/diagnostics/omega_report_data.json
