══════════════════════════════════════════════════════════════════════
ℹ️  OMEGA REPORT — RENDERIZADOR PURO
  Versión Omega: 12.2-puro
  Omega no crea datos. Solo imprime el paquete entregado por Engine.
══════════════════════════════════════════════════════════════════════

══════════════════════════════════════════════════════════════════════
  ▶️  INFORMACIÓN DEL RUN
══════════════════════════════════════════════════════════════════════
  version_engine: 20
  estado_engine: OPERATIVO
  esquema_contrato: VPSI-CONTRACT-1.0
  total_modulos: 19
  trazas_n: 55
  rutas_n: 0
  timestamp: 2026-08-20T07:43:53.275095+00:00

══════════════════════════════════════════════════════════════════════
  INFORMACIÓN DEL RUN
══════════════════════════════════════════════════════════════════════
  version_engine: 20
  esquema_contrato: VPSI-CONTRACT-1.0
  version_contrato_requerida: 1.0
  api_engine: 1.0
  estado_engine: OPERATIVO
  invocador_id: omega_report
  total_modulos: 19
  errores_arranque:
    []
  advertencias:
    []
  trazas_n: 55
  rutas_n: 0
  timestamp: 2026-08-20T07:43:53.275016+00:00

══════════════════════════════════════════════════════════════════════
  MÓDULO AX/axiomas
══════════════════════════════════════════════════════════════════════
  id: AX
  nombre: axiomas
  rol: AX
  version: 8.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 9.5
  api_engine: >=1.0
  descripcion: Responsable del conocimiento axiomático del sistema. Mantiene, valida, organiza y expone todas las declaraciones oficiales del repositorio a ENGINE.
  funcion: Ser la fuente oficial del conocimiento axiomático: cargar, normalizar, validar coherencia, responder consultas, citar declaraciones, exponer generatividad y determinar el límite axiomático.
  no_hace:
    • No calcula Tru_total ni Tru_Ri
    • No orquesta el sistema (eso es Engine)
    • No genera reportes de otros módulos
  autoridad:
    • Exponer cualquier axioma, lema, teorema, corolario o definición
    • Responder consultas por id, dominio, sujeto, relación, objeto
    • Citar y relacionar declaraciones del grafo
    • Verificar coherencia interna
    • Reportar estado, salud, inventario y diagnóstico propios
    • Notificar a DiagnosticoGlobal cuando hay choques o errores
    • Determinar el límite de derivación axiomática
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
    • limite_axiomático
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
    • limite_axiomático
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
  autoriza_engine:
    leer: True
    consultar: True
    estado: True
    version: True
    salud: True
    capacidades: True
    contrato: True
    conocimiento: True
    dependencias: True
    ejecutar: True
    ejecutar_total: True
    procesar: True
    analizar: True
    generar: True
    validar: True
    validar_esquema: True
    inspeccionar: True
    inventariar: True
    registrar_inventario: True
    inventario: True
    acceso_archivos: True
    reportar: True
    reporte: True
    diagnostico: True
    metricas: True
    errores: True
    advertencias: True
    auditar: True
    monitorear: True
    recombinar: True
    sincronizar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    crear: True
    actualizar: False
    alterar: False
    evaluar_universal: True
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
    • limite_axiomático
    • ejecutar_total
    • inspeccionar
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia interna del módulo.
      entrada: declaraciones_externas opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con coherente, choques, errores, declaraciones, cuerpos, por_tipo
      acceso_archivos:
        • acceso_archivos
    barrer:
      descripcion: Analiza coherencia de todas las declaraciones (contradicción directa y de cota).
      entrada: declaraciones_externas opcional (dict)
      validar_esquema:
        • *
      salida: dict con coherente, choques, errores, declaraciones, cuerpos, por_tipo, ids_dominio_k_o
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Comprueba si una salida de barrer/verificar es coherente.
      entrada: salida: dict
      validar_esquema:
        • validar_esquema
      salida: bool
      acceso_archivos:
        • acceso_archivos
    inventario:
      descripcion: Inventario completo del módulo (declaraciones, cuerpos, capacidades).
      entrada: peticion
      validar_esquema:
        • acceso_archivos
      salida: dict con id, nombre, rol, version, declaraciones, cuerpos, capacidades
      acceso_archivos:
        • acceso_archivos
    axiomas:
      descripcion: Devuelve las declaraciones si el módulo es coherente; lista vacía si no.
      entrada: declaraciones_externas opcional (dict)
      validar_esquema:
        • *
      salida: list[dict] de declaraciones normalizadas
      acceso_archivos:
        • *
    declaraciones:
      descripcion: Igual que axiomas: declaraciones normalizadas si coherente.
      entrada: declaraciones_externas opcional (dict)
      validar_esquema:
        • *
      salida: list[dict] de declaraciones normalizadas
      acceso_archivos:
        • *
    generatividad:
      descripcion: Mide generatividad operativa y canónica (TR1).
      entrada: acceso_archivos
      validar_esquema:
        • acceso_archivos
      salida: dict con theta_n, pares, im_vs_theta, capa canonica, dominios, u1_proxy
      acceso_archivos:
        • acceso_archivos
    por_dominio:
      descripcion: Filtra declaraciones por dominio en gobierna.
      entrada: dominio: str; declaraciones_externas opcional
      validar_esquema:
        • acceso_archivos
      salida: list[dict] de declaraciones del dominio
      acceso_archivos:
        • acceso_archivos
    ids_dominio_k_o:
      descripcion: Ids de declaraciones ligadas a dominios K/O o Def-5.3.1.
      entrada: declaraciones_externas (dict)
      validar_esquema:
        • acceso_archivos
      salida: list[str] de ids ordenados
      acceso_archivos:
        • acceso_archivos
    recolectar:
      descripcion: Carga y normaliza todas las declaraciones de los cuerpos del módulo.
      entrada: declaraciones_externas opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: tuple[list[dict], list[dict]] → (declaraciones, errores)
      acceso_archivos:
        • acceso_archivos
    reporte:
      descripcion: Reporte interno de estado del módulo.
      entrada: acceso_archivos
      validar_esquema:
        • *
      salida: dict con estado, coherente, declaraciones, choques, errores, capacidades
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico: qué me sucede, qué falta, qué está mal, qué necesito.
      entrada: acceso_archivos
      validar_esquema:
        • acceso_archivos
      salida: dict con estado, problemas, advertencias, recomendaciones, limites
      acceso_archivos:
        • acceso_archivos
    buscar_por_id:
      descripcion: Busca y cita una declaración por su id.
      entrada: id_decl: str
      validar_esquema:
        • acceso_archivos
      salida: dict de la declaración o None
      acceso_archivos:
        • acceso_archivos
    limite_axiomático:
      descripcion: Determina el límite de derivación axiomática: premisas disponibles, premisas faltantes, dependencias no satisfechas, alcance y declaraciones no derivables.
      entrada: declaraciones_externas opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con premisas_disponibles, premisas_faltantes, dependencias_no_satisfechas, limites, alcance
      acceso_archivos:
        • acceso_archivos
    ejecutar_total:
      descripcion: Operación arquitectónica genérica. Ejerce la totalidad de las unidades operativamente ejecutables del módulo conforme a su contrato e inventario.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspección estructural del módulo. Expone el estado interno, componentes y unidades ejecutables sin alterar el contrato.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del módulo
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
    • una conclusión solo se reconoce como sustentada si sus premisas están en el cuerpo axiomático
    • ausencia de premisa no se convierte en axioma
    • contradicción y límite axiomático son estados distintos
  reporte:
    id: AX
    modulo: axiomas
    rol: AX
    version: 8.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    declaraciones: 748
    choques: 0
    errores: 0
    cuerpos:
      • Anclas_de_Medicion_AM_AX
      • VPSI_AX
      • contexto_AX
      • correlacion_AX
      • diccionario_AX
      • entendimiento_fractal_AX
      • estructura_pensamiento_AX
      • indefinido_AX
      • ley_coherencia_AX
      • metaconciencia_AX
      • peticion_anuncio_AX
      • principio_asociacion_AX
      • realidad_AX
      • self
      • sentido_estructural_AX
      • siete_capas_SL_AX
      • sm_af_AX
      • sm_mapa_AX
      • sm_memoria_AX
      • sm_precision_AX
      • teorema_conciencia_AX
      • teorema_forma_AX
      • teorema_luz_AX
    por_tipo:
      axioma: 225
      lema: 94
      teorema: 157
      corolario: 169
      definicion: 103
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
      • limite_axiomático
      • ejecutar_total
      • inspeccionar
      • evaluar_universal
    capacidades_resueltas:
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
      • limite_axiomático
      • ejecutar_total
      • inspeccionar
      • evaluar_universal
    capacidades_meta:
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
      • limite_axiomático
      • ejecutar_total
      • inspeccionar
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
    autoridad:
      • Exponer cualquier axioma, lema, teorema, corolario o definición
      • Responder consultas por id, dominio, sujeto, relación, objeto
      • Citar y relacionar declaraciones del grafo
      • Verificar coherencia interna
      • Reportar estado, salud, inventario y diagnóstico propios
      • Notificar a DiagnosticoGlobal cuando hay choques o errores
      • Determinar el límite de derivación axiomática
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
      • limite_axiomático
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
      • limite_axiomático
    limite_axiomático:
      premisas_faltantes: 31
      dependencias_no_satisfechas: 31
      dependencias_circulares: 0
    operaciones_arquitectonicas:
      verificar: True
      barrer: True
      verificar_salida: True
      inventario: True
      axiomas: True
      declaraciones: True
      generatividad: True
      por_dominio: True
      ids_dominio_k_o: True
      recolectar: True
      reporte: True
      diagnostico: True
      buscar_por_id: True
      limite_axiomático: True
      ejecutar_total: True
      inspeccionar: True
      evaluar_universal: True
  diagnostico:
    id: AX
    modulo: axiomas
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      • Existen declaraciones cuyas premisas no están en el cuerpo axiomático
    limites:
      [0]
        tipo: PREMISA_FALTANTE
        cantidad: 31
        detalle:
          [0]
            declaracion: AM-D1
            tipo: definicion
            faltantes:
              [0]
                id: Def-5.1
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D1
                  • Def-5.1
                nivel: 1
                razon: La dependencia declarada no existe en la instantánea disponible.
              [1]
                id: Def-5.2
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D1
                  • Def-5.2
                nivel: 1
                razon: La dependencia declarada no existe en la instantánea disponible.
              [2]
                id: Def-5.3
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D1
                  • Def-5.3
                nivel: 1
                razon: La dependencia declarada no existe en la instantánea disponible.
            ubicacion: Anclas_de_Medicion_AM_AX:AM-D1
          [1]
            declaracion: AM-D2
            tipo: definicion
            faltantes:
              [0]
                id: Def-5.1
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D2
                  • AM-D1
                  • Def-5.1
                nivel: 2
                razon: La dependencia declarada no existe en la instantánea disponible.
              [1]
                id: Def-5.2
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D2
                  • AM-D1
                  • Def-5.2
                nivel: 2
                razon: La dependencia declarada no existe en la instantánea disponible.
              [2]
                id: Def-5.3
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D2
                  • AM-D1
                  • Def-5.3
                nivel: 2
                razon: La dependencia declarada no existe en la instantánea disponible.
            ubicacion: Anclas_de_Medicion_AM_AX:AM-D2
          [2]
            declaracion: AM-D3
            tipo: definicion
            faltantes:
              [0]
                id: Def-5.1
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D3
                  • AM-D1
                  • Def-5.1
                nivel: 2
                razon: La dependencia declarada no existe en la instantánea disponible.
              [1]
                id: Def-5.2
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D3
                  • AM-D1
                  • Def-5.2
                nivel: 2
                razon: La dependencia declarada no existe en la instantánea disponible.
              [2]
                id: Def-5.3
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D3
                  • AM-D1
                  • Def-5.3
                nivel: 2
                razon: La dependencia declarada no existe en la instantánea disponible.
            ubicacion: Anclas_de_Medicion_AM_AX:AM-D3
          [3]
            declaracion: AM-D4
            tipo: definicion
            faltantes:
              [0]
                id: Def-5.1
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D4
                  • AM-D1
                  • Def-5.1
                nivel: 2
                razon: La dependencia declarada no existe en la instantánea disponible.
              [1]
                id: Def-5.2
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D4
                  • AM-D1
                  • Def-5.2
                nivel: 2
                razon: La dependencia declarada no existe en la instantánea disponible.
              [2]
                id: Def-5.3
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D4
                  • AM-D1
                  • Def-5.3
                nivel: 2
                razon: La dependencia declarada no existe en la instantánea disponible.
            ubicacion: Anclas_de_Medicion_AM_AX:AM-D4
          [4]
            declaracion: AM-D5
            tipo: definicion
            faltantes:
              [0]
                id: Def-5.1
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D5
                  • AM-D2
                  • AM-D1
                  • Def-5.1
                nivel: 3
                razon: La dependencia declarada no existe en la instantánea disponible.
              [1]
                id: Def-5.2
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D5
                  • AM-D2
                  • AM-D1
                  • Def-5.2
                nivel: 3
                razon: La dependencia declarada no existe en la instantánea disponible.
              [2]
                id: Def-5.3
                tipo: NO ENTREGADO POR ENGINE
                cadena_dependencia:
                  • AM-D5
                  • AM-D2
                  • AM-D1
                  • Def-5.3
                nivel: 3
                razon: La dependencia declarada no existe en la instantánea disponible.
            ubicacion: Anclas_de_Medicion_AM_AX:AM-D5
    coherente: True
    declaraciones: 748
    choques_n: 0
    errores_n: 0
    premisas_faltantes_n: 31
  inventario:
    id: AX
    nombre: axiomas
    rol: AX
    version: 8.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    compatible_desde: 9.5
    api_engine: >=1.0
    descripcion: Responsable del conocimiento axiomático del sistema. Mantiene, valida, organiza y expone todas las declaraciones oficiales del repositorio a ENGINE.
    funcion: Ser la fuente oficial del conocimiento axiomático: cargar, normalizar, validar coherencia, responder consultas, citar declaraciones, exponer generatividad y determinar el límite axiomático.
    no_hace:
      • No calcula Tru_total ni Tru_Ri
      • No orquesta el sistema (eso es Engine)
      • No genera reportes de otros módulos
    tipos:
      • axioma
      • lema
      • teorema
      • corolario
      • definicion
    declaraciones: 748
    por_tipo:
      axioma: 225
      lema: 94
      teorema: 157
      corolario: 169
      definicion: 103
    cuerpos:
      • Anclas_de_Medicion_AM_AX
      • VPSI_AX
      • contexto_AX
      • correlacion_AX
      • diccionario_AX
      • entendimiento_fractal_AX
      • estructura_pensamiento_AX
      • indefinido_AX
      • ley_coherencia_AX
      • metaconciencia_AX
      • peticion_anuncio_AX
      • principio_asociacion_AX
      • realidad_AX
      • self
      • sentido_estructural_AX
      • siete_capas_SL_AX
      • sm_af_AX
      • sm_mapa_AX
      • sm_memoria_AX
      • sm_precision_AX
      • teorema_conciencia_AX
      • teorema_forma_AX
      • teorema_luz_AX
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
      • limite_axiomático
      • ejecutar_total
      • inspeccionar
      • evaluar_universal
    capacidades_resueltas:
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
      • limite_axiomático
      • ejecutar_total
      • inspeccionar
      • evaluar_universal
    capacidades_meta:
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
      • limite_axiomático
      • ejecutar_total
      • inspeccionar
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
    autoridad:
      • Exponer cualquier axioma, lema, teorema, corolario o definición
      • Responder consultas por id, dominio, sujeto, relación, objeto
      • Citar y relacionar declaraciones del grafo
      • Verificar coherencia interna
      • Reportar estado, salud, inventario y diagnóstico propios
      • Notificar a DiagnosticoGlobal cuando hay choques o errores
      • Determinar el límite de derivación axiomática
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
      • limite_axiomático
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
      • limite_axiomático
    autoriza_engine:
      leer: True
      consultar: True
      estado: True
      version: True
      salud: True
      capacidades: True
      contrato: True
      conocimiento: True
      dependencias: True
      ejecutar: True
      ejecutar_total: True
      procesar: True
      analizar: True
      generar: True
      validar: True
      validar_esquema: True
      inspeccionar: True
      inventariar: True
      registrar_inventario: True
      inventario: True
      acceso_archivos: True
      reportar: True
      reporte: True
      diagnostico: True
      metricas: True
      errores: True
      advertencias: True
      auditar: True
      monitorear: True
      recombinar: True
      sincronizar: True
      exportar: True
      importar: True
      respaldar: True
      recuperar: True
      crear: True
      actualizar: False
      alterar: False
      evaluar_universal: True
    reporting:
      estado: True
      salud: True
      version: True
      inventario: True
      capacidades: True
      acceso_archivos: True
      ejecutar_total: True
      inspeccionar: True
      registrar_inventario: True
      errores: True
      advertencias: True
      dependencias: True
      contrato: True
      conocimiento: True
      metricas: True
      diagnostico: True
      reporte: True
      validar_esquema: True
      evaluar_universal: True
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
      • una conclusión solo se reconoce como sustentada si sus premisas están en el cuerpo axiomático
      • ausencia de premisa no se convierte en axioma
      • contradicción y límite axiomático son estados distintos
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
      • AF-A1
      • AF-A2
      • AF-A3
      • AF-C1
      • AF-C3
      • AF-C4
      • AF-C5
      • AF-D3
      • AF-T1
      • AF-T2
      • AF-T4
      • AF-T5
      • AF-T6
      • AF-T7
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
      • DIC-A2
      • DIC-D1
      • DIC-L1
      • DIC-L2
      • Def-5.3.1
      • E1
      • E2
      • E3
      • EF-A1
      • EF-A2
      • EF-A3
      • EF-A4
      • EF-A5
      • EF-A7
      • EF-C1
      • EF-C2
      • EF-C3
      • EF-C4
      • EF-C5
      • EF-D1
      • EF-D2
      • EF-D3
      • EF-D4
      • EF-D5
      • EF-L1
      • EF-L3
      • EF-T1
      • EF-T2
      • EF-T3
      • EF-T4
      • EF-T5
      • EF-T6
      • I
      • IND-A1
      • IND-A2
      • IND-A3
      • IND-A4
      • IND-A5
      • IND-C1
      • IND-C2
      • IND-C3
      • IND-C4
      • IND-C5
      • IND-C6
      • IND-D1
      • IND-D2
      • IND-D3
      • IND-D4
      • IND-D5
      • IND-L1
      • IND-L2
      • IND-L3
      • IND-L4
      • IND-T1
      • IV
      • LC-A1
      • LC-A2
      • LC-A3
      • LC-C1
      • LC-C2
      • LC-C3
      • LC-D1
      • LC-D2
      • LC-L1
      • LC-L2
      • LC-T1
      • LC-T2
      • M.1
      • MC-A1
      • MC-A2
      • MC-A3
      • MC-A4
      • MC-A5
      • MC-A6
      • MC-A7
      • MC-A8
      • MC-C1
      • MC-C2
      • MC-C3
      • MC-D1
      • MC-D2
      • MC-D3
      • MC-D4
      • MC-L1
      • MC-L2
      • MC-L3
      • MC-T1
      • MC-T2
      • MC-T3
      • PA-A2
      • PA-D3
      • PA-T1
      • PA-T3
      • PDA-A1
      • PDA-A10
      • PDA-A2
      • PDA-A3
      • PDA-A4
      • PDA-A5
      • PDA-A6
      • PDA-A7
      • PDA-A8
      • PDA-A9
      • PDA-C1
      • PDA-C2
      • PDA-C3
      • PDA-C4
      • PDA-C5
      • PDA-C6
      • PDA-C7
      • PDA-C8
      • PDA-D1
      • PDA-D10
      • PDA-D2
      • PDA-D3
      • PDA-D4
      • PDA-D5
      • PDA-D6
      • PDA-D7
      • PDA-D8
      • PDA-D9
      • PDA-L1
      • PDA-L2
      • PDA-L3
      • PDA-L4
      • PDA-L5
      • PDA-L6
      • PDA-L7
      • PDA-L8
      • PDA-L9
      • PDA-T1
      • PDA-T2
      • PDA-T3
      • PDA-T4
      • PDA-T5
      • PDA-T6
      • PDA-T7
      • RE-A0
      • RE-A1
      • RE-A10
      • RE-A2
      • RE-A3
      • RE-A4
      • RE-A5
      • RE-A6
      • RE-A7
      • RE-A8
      • RE-A9
      • RE-C1
      • RE-C3
      • RE-C6
      • RE-C8
      • RE-L1
      • RE-L2
      • RE-L4
      • RE-L5
      • RE-T1
      • RE-T10
      • RE-T11
      • RE-T12
      • RE-T13
      • RE-T2
      • RE-T3
      • RE-T4
      • RE-T5
      • RE-T7
      • RE-T8
      • RE-T9
      • SE-A0
      • SE-A1
      • SE-A3
      • SE-A5
      • SE-A6
      • SE-C2
      • SE-C3
      • SE-C4
      • SE-D1
      • SE-D4
      • SE-D5
      • SE-L2
      • SE-T1
      • SE-T3
      • SE-T4
      • SL-A1
      • SL-A2
      • SL-A3
      • SL-A4
      • SL-A5
      • SL-A6
      • SL-A7
      • SL-C12
      • SL-C13
      • SL-C14
      • SL-C15
      • SL-C16
      • SL-C17
      • SL-C18
      • SL-D1
      • SL-D10
      • SL-D2
      • SL-D3
      • SL-D4
      • SL-D5
      • SL-D6
      • SL-D7
      • SL-D8
      • SL-D9
      • SL-T11
      • SM-A12
      • SM-A2
      • SM-A3
      • SM-A4
      • SM-A6
      • SM-A8
      • SM-C1
      • SM-C10
      • SM-C3
      • SM-C7
      • SM-D1
      • SM-D2
      • SM-D5
      • SM-D6
      • SM-L2
      • SM-L4
      • SM-L9
      • SM-T1
      • SM-T2
      • SM-T4
      • SM-T6
      • SM-T9
      • ST-A1
      • ST-A2
      • ST-C1
      • ST-C2
      • ST-C3
      • ST-C4
      • ST-D1
      • ST-D2
      • ST-D3
      • ST-D4
      • ST-D5
      • ST-D6
      • ST-L1
      • ST-L2
      • ST-L3
      • ST-T1
      • ST-T2
      • ST-T3
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
      • TA4
      • TC-A1
      • TC-A2
      • TC-A3
      • TC-A4
      • TC-A5
      • TC-A6
      • TC-A7
      • TC-C1
      • TC-C2
      • TC-C3
      • TC-C4
      • TC-C5
      • TC-C6
      • TC-D1
      • TC-D2
      • TC-D3
      • TC-D4
      • TC-D5
      • TC-D6
      • TC-D7
      • TC-L1
      • TC-L2
      • TC-L3
      • TC-L4
      • TC-L5
      • TC-T1
      • TC-T2
      • TC-T3
      • TC-T4
      • TC-T5
      • TF-A1
      • TF-A2
      • TF-A3
      • TF-A4
      • TF-A5
      • TF-A6
      • TF-B1
      • TF-C1
      • TF-C1-D
      • TF-C2
      • TF-C2-D
      • TF-C3
      • TF-C3-D
      • TF-C4
      • TF-C4-D
      • TF-C5
      • TF-C6
      • TF-D1
      • TF-D1-D
      • TF-D2
      • TF-D2-D
      • TF-D3
      • TF-D3-D
      • TF-D4-D
      • TF-D5-D
      • TF-L1
      • TF-L1-D
      • TF-L2
      • TF-L2-D
      • TF-L3
      • TF-L3-D
      • TF-T1
      • TF-T2
      • TF-T3
      • TL-A1
      • TL-A2
      • TL-A3
      • TL-A4
      • TL-A5
      • TL-A6
      • TL-A7
      • TL-A8
      • TL-C1
      • TL-C2
      • TL-C3
      • TL-C4
      • TL-C5
      • TL-D1
      • TL-D2
      • TL-D3
      • TL-D4
      • TL-D5
      • TL-D6
      • TL-D7
      • TL-L1
      • TL-L2
      • TL-L3
      • TL-L4
      • TL-L5
      • TL-L6
      • TL-L7
      • TL-L8
      • TL-T1
      • TL-T2
      • TL-T3
      • TL-T4
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
    limite_axiomático:
      premisas_faltantes: 31
      dependencias_no_satisfechas: 31
      dependencias_circulares: 0
      alcance:
        total_declaraciones: 748
        dependencias_no_satisfechas: 31
        premisas_faltantes: 31
    operaciones_arquitectonicas:
      ejecutar_total: True
      inspeccionar: True
    nota: Inventario estructural. La información se construye sobre una única recolección. ids_dominio_k_o se determina mediante la misma regla estructural de 8.2 sobre esa instantánea, sin invocar nuevamente la callable. limite_axiomático se reporta como información estructural y no como criterio adicional de coherencia.

══════════════════════════════════════════════════════════════════════
  MÓDULO CH/cache
══════════════════════════════════════════════════════════════════════
  id: CH
  nombre: cache
  rol: CH
  version: 4.1
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Registrador universal de eventos. Libro de actas del sistema. Mapeo estructural del código accesible. Clasificación de IDs por módulo y detección de duplicados. Conserva evidencia objetiva. Categorías dinámicas. No interpreta. No deduce. No reconstruye semánticamente. No calcula.
  funcion: Registrar exactamente lo que ocurrió durante la ejecución, exponer lecturas filtradas por campos del registro, mapear la estructura del código accesible y clasificar IDs por módulo incluyendo duplicados. Nada más.
  no_hace:
    • No interpreta
    • No deduce ni infiere
    • No reconstruye ciclos semánticamente
    • No genera grafos interpretativos ni árboles de causalidad
    • No explica razonamientos ni causas
    • No calcula C / L / K / Tru
    • No descubre relaciones semánticas
    • No altera evidencia depositada
    • No inicia operaciones de otros módulos
    • No envía reportes a otros módulos
    • No ejecuta funciones descubiertas durante el mapeo
  autoridad:
    • Registrar eventos depositados por Engine o Centinela
    • Entregar lecturas filtradas por campos del registro
    • Exponer categorías descubiertas dinámicamente
    • Verificar integridad del registro (forma, no contenido)
    • Mapear estructura del código accesible
    • Clasificar IDs por módulo y reportar duplicados
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
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • mapear_codigo
    • clasificar_ids
  consultas_soportadas:
    • depositar_evento
    • leer_eventos
    • filtrar_por_campo
    • listar_categorias
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • verificar_integridad_registro
    • mapear_codigo
    • clasificar_ids
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    evaluar_universal: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
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
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • mapear_codigo
    • clasificar_ids
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Integridad formal del registro.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con coherente, inmutable, errores, resumen
      acceso_archivos:
        • *
    barrer:
      descripcion: Verifica forma del registro: seq creciente, timestamps, payload dict. No interpreta contenido. No mapea código.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con coherente, inmutable, errores, resumen
      acceso_archivos:
        • *
    depositar:
      descripcion: Registra un evento neutro. Única vía de escritura. Append-only. Categorías se descubren al depositar.
      entrada: tipo, payload, ciclo_id?, run_id?, origen?, destino?, modulo?, capacidad?, categoria?, estado?
      validar_esquema:
        • *
      salida: dict del evento registrado
      acceso_archivos:
        • *
    leer:
      descripcion: Lectura genérica con filtros opcionales por campo.
      entrada: filtros opcionales por campo del registro
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_eventos:
      descripcion: Alias de leer sin filtros (todos los eventos).
      entrada: ninguna
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_por_ciclo:
      descripcion: Eventos de un ciclo_id.
      entrada: ciclo_id: str
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_por_modulo:
      descripcion: Eventos de un módulo.
      entrada: modulo: str, ciclo_id?
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_por_tipo:
      descripcion: Eventos de un tipo.
      entrada: tipo: str, ciclo_id?
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_por_categoria:
      descripcion: Eventos de una categoría (dinámica).
      entrada: categoria: str, ciclo_id?
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_por_capacidad:
      descripcion: Eventos de una capacidad.
      entrada: capacidad: str, ciclo_id?
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_por_origen:
      descripcion: Eventos con un origen dado.
      entrada: origen: str, ciclo_id?
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_por_destino:
      descripcion: Eventos con un destino dado.
      entrada: destino: str, ciclo_id?
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_por_estado:
      descripcion: Eventos con un estado dado.
      entrada: estado: str, ciclo_id?
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_por_seq:
      descripcion: Eventos en un rango de seq.
      entrada: desde_seq?, hasta_seq?
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    leer_por_timestamp:
      descripcion: Eventos en un rango de timestamp.
      entrada: desde_timestamp?, hasta_timestamp?
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    categorias:
      descripcion: Categorías descubiertas dinámicamente hasta ahora.
      entrada: ninguna
      validar_esquema:
        • *
      salida: list[str]
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario del módulo, resumen del registro y, si disponible, inventario estructural mapeado.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con id, version, memoria, categorias, capacidades, estructura
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte interno de estado del módulo CH.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con estado, coherente, memoria, capacidades
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico de integridad formal del registro.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Comprueba forma de una salida de barrer o depósito.
      entrada: salida: dict
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    backend_para_centinela:
      descripcion: Adaptador estable CacheBackend para Centinela. Centinela no conoce la implementación interna.
      entrada: ninguna
      validar_esquema:
        • *
      salida: CacheBackend
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Operación arquitectónica genérica. Ejerce la totalidad de las unidades operativamente ejecutables del módulo conforme a su contrato e inventario.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspección estructural del módulo. Expone capacidades contractuales, callables reales, estructura descubierta, IDs y duplicados.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del módulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural del módulo sin alterar evidencia depositada.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    mapear_codigo:
      descripcion: Recorre el código accesible a CACHE y obtiene la estructura real: módulos, archivos, IDs, funciones, métodos, clases, callables y capacidades declaradas. No interpreta semántica. No ejecuta funciones descubiertas.
      entrada: peticion opcional (dict con raiz?)
      validar_esquema:
        • *
      salida: dict con inventario estructural completo
      acceso_archivos:
        • *
    clasificar_ids:
      descripcion: Clasifica IDs por módulo a partir del inventario estructural. Separa IDs únicos de IDs duplicados. Un duplicado es clasificación estructural, no error automático.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con ids_por_modulo, ids_unicos, ids_duplicados, id_a_modulos
      acceso_archivos:
        • *
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
    • este módulo no reconstruye ni genera grafos interpretativos
    • la evidencia depositada nunca se modifica
    • la evidencia depositada nunca se sobrescribe
    • la evidencia depositada nunca se reordena
    • la evidencia depositada nunca desaparece durante el ciclo
    • toda información nueva se incorpora solo como evento nuevo
    • las categorías son dinámicas; no hay lista fija de dominios
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
    • el mapeo estructural no ejecuta funciones descubiertas
    • un ID duplicado se clasifica, no se borra ni se interpreta como error automático
  reporte:
    id: CH
    modulo: cache
    rol: CH
    version: 4.1
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • mapear_codigo
      • clasificar_ids
      • evaluar_universal
    capacidades_meta:
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • mapear_codigo
      • clasificar_ids
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    autoridad:
      • Registrar eventos depositados por Engine o Centinela
      • Entregar lecturas filtradas por campos del registro
      • Exponer categorías descubiertas dinámicamente
      • Verificar integridad del registro (forma, no contenido)
      • Mapear estructura del código accesible
      • Clasificar IDs por módulo y reportar duplicados
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • mapear_codigo
      • clasificar_ids
    consultas_soportadas:
      • depositar_evento
      • leer_eventos
      • filtrar_por_campo
      • listar_categorias
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • verificar_integridad_registro
      • mapear_codigo
      • clasificar_ids
    operaciones_arquitectonicas:
      ejecutar_total: True
      inspeccionar: True
      registrar_inventario: True
      mapear_codigo: True
      clasificar_ids: True
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
    version: 4.1
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    funcion: Registrador universal de eventos. Libro de actas. Mapeo estructural. Clasificación de IDs. Append-only.
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • mapear_codigo
      • clasificar_ids
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no calcula
      • este módulo no interpreta
      • este módulo no deduce ni infiere
      • este módulo no reconstruye ni genera grafos interpretativos
      • la evidencia depositada nunca se modifica
      • la evidencia depositada nunca se sobrescribe
      • la evidencia depositada nunca se reordena
      • la evidencia depositada nunca desaparece durante el ciclo
      • toda información nueva se incorpora solo como evento nuevo
      • las categorías son dinámicas; no hay lista fija de dominios
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
      • el mapeo estructural no ejecuta funciones descubiertas
      • un ID duplicado se clasifica, no se borra ni se interpreta como error automático
    estructura:
      total_modulos: 19
      total_ids: 18
      total_unicos: 18
      total_duplicados: 0
      ids_duplicados:
      actualizado: 2026-08-20T07:43:53.072056+00:00
    nota: CACHE no sabe lo que ocurrió. Solo sabe qué fue registrado y qué estructura encontró. Análisis semántico: módulo futuro.

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
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
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
    • verificar_calculo_de_C_L_K
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  requiere:
    • CT
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
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
    • verificar_calculo_de_C_L_K
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    calcular:
      descripcion: Pipeline completo. C/L/K son objetos unicos con fraccion+decimal (ej display: 7/9 = 0.778).
      entrada: peticion: dict
      validar_esquema:
        • *
      salida: dict con id_calculo, C, L, K, evidencia, versiones_utilizadas, centinela, errores
      acceso_archivos:
        • *
    calcular_C:
      descripcion: Factor C como objeto fraccion+decimal.
      entrada: peticion: dict
      validar_esquema:
        • *
      salida: dict con C, ruta, notas, evidencia
      acceso_archivos:
        • *
    calcular_L:
      descripcion: Factor L como objeto (o UNDEFINED).
      entrada: peticion: dict
      validar_esquema:
        • *
      salida: dict con L, p, r, ruta, notas, evidencia
      acceso_archivos:
        • *
    calcular_K:
      descripcion: Factor K como objeto (o None sin O).
      entrada: peticion: dict
      validar_esquema:
        • *
      salida: dict con K, ruta, notas, evidencia
      acceso_archivos:
        • *
    calcular_factor:
      descripcion: Factor por nombre C|L|K.
      entrada: factor: str, peticion: dict
      validar_esquema:
        • *
      salida: dict del factor
      acceso_archivos:
        • *
    representar:
      descripcion: Fraction -> objeto con fraccion, numerador, denominador, decimal, display (7/9 = 0.778). Sin float.
      entrada: valor: Fraction|UNDEFINED|None, precision: int=3
      validar_esquema:
        • *
      salida: dict valor completo
      acceso_archivos:
        • *
    validar_evidencia:
      descripcion: Valida lista de evidencia sin calcular: estructura, rechazados, conflicto de versiones del mismo modulo.
      entrada: evidencia: list[dict]
      validar_esquema:
        • *
      salida: dict con ok, problemas, advertencias, evidencia_normalizada
      acceso_archivos:
        • *
    explicar_calculo:
      descripcion: Explica un calculo por id usando evidencia real almacenada.
      entrada: id_calculo: str
      validar_esquema:
        • *
      salida: dict explicativo dinamico o None
      acceso_archivos:
        • *
    verificar:
      descripcion: Centinela de integridad (APIs, hashes, choques).
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con coherente, errores, choques, hashes
      acceso_archivos:
        • *
    barrer:
      descripcion: Alias de verificar.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con coherente, errores, choques, hashes
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario del dominio de calculo.
      entrada: peticion opcional
      validar_esquema:
        • *
      salida: dict con capacidades, factores, archivos, hashes
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte de estado de CA.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con estado, coherente, factores_api
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnostico de problemas y recomendaciones.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    leer_ids_escala:
      descripcion: Ids de escala reconocidos.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con ids, n, origenes
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Forma minima: C, L, K, id_calculo; cada factor con display.
      entrada: salida: dict
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    historial:
      descripcion: Buffer liviano de ultimos calculos.
      entrada: limite opcional: int
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    verificar_calculo_de_C_L_K:
      descripcion: Verifica la integridad y coherencia del calculo de C, L y K.
      entrada: calculo: dict
      validar_esquema:
        • *
      salida: dict con valido, errores, advertencias, C, L, K y verificacion
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre CA. Ejerce TODAS las unidades operativamente ejecutables del modulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de CA. Expone constantes, capacidades, APIs y estado sin alterar el contrato ni calcular factores.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de CA como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
    apis_factor:
      C: True
      L: True
      K: True
    archivos:
      • coherencia.py
      • conteos.py
      • correlacion_k.py
      • escalas_ids.py
      • logica.py
    archivos_extra:
      []
    hashes:
      __init__.py:
        archivo: __init__.py
        sha256: 39c403d502cb9f5d3785c4860e832654016d3ca22647fc1cb23fdc4dd9b0c41e
        tamano: 166998
        timestamp_mtime: 2026-08-20T07:43:47.760913+00:00
      coherencia.py:
        archivo: coherencia.py
        sha256: 3eba01b69ffd993205a3e7963d1ecfb564246dee8d737d7a1506f74247edcf34
        tamano: 6365
        timestamp_mtime: 2026-08-20T07:43:47.762106+00:00
      conteos.py:
        archivo: conteos.py
        sha256: 19c30b65365863ef671d9e03aba20e9096b97033681120c4c9ca49dadf352330
        tamano: 20987
        timestamp_mtime: 2026-08-20T07:43:47.762106+00:00
      correlacion_k.py:
        archivo: correlacion_k.py
        sha256: b1cc60d3cc07db792ad4978ff6b14f810d406a62aeae6f552b1795d6695200ab
        tamano: 5546
        timestamp_mtime: 2026-08-20T07:43:47.762106+00:00
      escalas_ids.py:
        archivo: escalas_ids.py
        sha256: 1db219e396c1a9c1cbfdf29ff92842b2b151907c07c6043a70c46349661ba128
        tamano: 2895
        timestamp_mtime: 2026-08-20T07:43:47.762106+00:00
      logica.py:
        archivo: logica.py
        sha256: 39b805c383a02e670d4fd1158e0c95b8e2e41c2d451c8ca377f497c802c236f1
        tamano: 4803
        timestamp_mtime: 2026-08-20T07:43:47.762106+00:00
    conteos_disponible: True
    escalas_ids_disponible: True
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
      • verificar_calculo_de_C_L_K
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    capacidades_callable:
      • barrer
      • calcular
      • calcular_C
      • calcular_K
      • calcular_L
      • calcular_factor
      • diagnostico
      • ejecutar_total
      • evaluar_universal
      • explicar_calculo
      • historial
      • inspeccionar
      • inventario
      • leer_ids_escala
      • registrar_inventario
      • reporte
      • representar
      • validar_evidencia
      • verificar
      • verificar_calculo_de_C_L_K
      • verificar_salida
    operaciones_arquitectonicas:
      ejecutar_total: True
      inspeccionar: True
      registrar_inventario: True
    autoridad:
      • Unica autoridad para calcular C, L, K
      • Reportar cada factor como fraccion = decimal en un solo objeto
      • Validar evidencia y explicar calculos con trazabilidad real
      • Auditar integridad del dominio
    autoriza_engine:
      leer: True
      ejecutar: True
      consultar: True
      recombinar: True
      reportar: True
      auditar: True
      inventariar: True
      alterar: False
      crear: True
      actualizar: False
      validar: True
      procesar: True
      analizar: True
      generar: True
      exportar: True
      importar: True
      respaldar: True
      recuperar: True
      sincronizar: True
      monitorear: True
      metricas: True
      diagnostico: True
      estado: True
      version: True
      salud: True
      inventario: True
      capacidades: True
      errores: True
      advertencias: True
      dependencias: True
      contrato: True
      conocimiento: True
      reporte: True
      validar_esquema: True
      acceso_archivos: True
      ejecutar_total: True
      inspeccionar: True
      registrar_inventario: True
      evaluar_universal: True
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
    regla_salida: un objeto por factor: fraccion = decimal
  diagnostico:
    id: CA
    modulo: calculator
    estado: OPERATIVO
    coherente: True
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    factores_api:
      • C
      • K
      • L
    apis_factor:
      C: True
      L: True
      K: True
    conteos_disponible: True
    escalas_ids_disponible: True
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
        sha256: 39c403d502cb9f5d3785c4860e832654016d3ca22647fc1cb23fdc4dd9b0c41e
        tamano: 166998
        timestamp_mtime: 2026-08-20T07:43:47.760913+00:00
      coherencia.py:
        archivo: coherencia.py
        sha256: 3eba01b69ffd993205a3e7963d1ecfb564246dee8d737d7a1506f74247edcf34
        tamano: 6365
        timestamp_mtime: 2026-08-20T07:43:47.762106+00:00
      conteos.py:
        archivo: conteos.py
        sha256: 19c30b65365863ef671d9e03aba20e9096b97033681120c4c9ca49dadf352330
        tamano: 20987
        timestamp_mtime: 2026-08-20T07:43:47.762106+00:00
      correlacion_k.py:
        archivo: correlacion_k.py
        sha256: b1cc60d3cc07db792ad4978ff6b14f810d406a62aeae6f552b1795d6695200ab
        tamano: 5546
        timestamp_mtime: 2026-08-20T07:43:47.762106+00:00
      escalas_ids.py:
        archivo: escalas_ids.py
        sha256: 1db219e396c1a9c1cbfdf29ff92842b2b151907c07c6043a70c46349661ba128
        tamano: 2895
        timestamp_mtime: 2026-08-20T07:43:47.762106+00:00
      logica.py:
        archivo: logica.py
        sha256: 39b805c383a02e670d4fd1158e0c95b8e2e41c2d451c8ca377f497c802c236f1
        tamano: 4803
        timestamp_mtime: 2026-08-20T07:43:47.762106+00:00
    factores_api:
      • C
      • K
      • L
    factores_no_declarados:
      []
    archivos_extra:
      []
    apis_factor:
      C: True
      L: True
      K: True
    conteos_disponible: True
    apis_conteos:
      extraer_conteos: True
      inyectar_en_peticion: True
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
    errores:
      []
    choques:
      []
    historial_n: 0
    capacidades:
      • barrer
      • calcular
      • calcular_C
      • calcular_K
      • calcular_L
      • calcular_factor
      • diagnostico
      • ejecutar_total
      • evaluar_universal
      • explicar_calculo
      • historial
      • inspeccionar
      • inventario
      • leer_ids_escala
      • registrar_inventario
      • reporte
      • representar
      • validar_evidencia
      • verificar
      • verificar_calculo_de_C_L_K
      • verificar_salida
    requiere:
      • AX
      • CA
      • CC
      • CH
      • CIT
      • CT
      • CX
      • DGCO
      • DI
      • FO
      • MC
      • RE
      • SC
      • SF
      • TT
      • TX
      • UI
      • VX
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
    regla_salida: cada factor se representa mediante su objeto contractual; cuando existe un valor definido, el objeto contiene fraccion, numerador, denominador, decimal y display

══════════════════════════════════════════════════════════════════════
  MÓDULO CE/capacidades_engine
══════════════════════════════════════════════════════════════════════
  id: CE
  nombre: capacidades_engine
  rol: CE
  version: 1.2
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Capacidad estructural del Engine: órgano único que agrupa múltiples skills nativos. Así como un brazo posee varias habilidades sin dejar de ser un solo órgano, CE agrupa skills sin ser un módulo de dominio. Los archivos son implementación física; los skills son competencias operativas; el mandato es la forma en que Engine los invoca. Engine no pide permiso a CE: los skills forman parte de su propia estructura. CE mantiene el inventario operativo de esas capacidades nativas.
  funcion: Mantener el inventario operativo de skills nativos del Engine. El descubrimiento automático de *.py actualiza ese inventario. Validar forma mínima y exponer ids/skills a Engine. No calcular. No depositar. No ejecutar. No decidir.
  no_hace:
    • No toma decisiones
    • No selecciona skills
    • No ejecuta skills (solo Engine ejecuta)
    • No coordina ciclos
    • No interpreta peticiones
    • No calcula C / L / K / Tru
    • No deposita evidencia
    • No orquesta el sistema
    • No compite con módulos de dominio (AX, CA, CH, TT, SF, …)
  autoridad:
    • Mantener el inventario operativo de skills nativos del Engine
    • Descubrir y validar forma mínima de cada skill
    • Exponer ids y skills a Engine
    • Reportar estado e inventario propios
  conocimiento_exportable:
    • skills
    • ids
    • por_id
    • listar_archivos
    • inventario
    • barrer
    • verificar
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  consultas_soportadas:
    • listar_skills
    • listar_ids
    • obtener_por_id
    • listar_archivos
    • obtener_inventario
    • verificar_coherencia
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  requiere:
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
  capacidades:
    • verificar
    • barrer
    • inventario
    • skills
    • ids
    • por_id
    • listar_archivos
    • verificar_salida
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • reporte
    • diagnostico
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. ¿El inventario operativo de skills de CE es coherente?
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, nombre, rol, version, coherente, ids, errores
      acceso_archivos:
        • *
    barrer:
      descripcion: Centinela de CE: valida forma de skills nativos. No decide, no ejecuta, no restringe uso.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, nombre, rol, version, coherente, ids, n, archivos
      acceso_archivos:
        • acceso_archivos
    inventario:
      descripcion: Inventario operativo de skills nativos del Engine expuestos por la capacidad CE.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, nombre, rol, version, version_contrato, esquema, estabilidad, ids, n, archivos, skills, coherente
      acceso_archivos:
        • *
    skills:
      descripcion: Lista de skills válidos (nombre histórico de la API).
      entrada: *
      validar_esquema:
        • *
      salida: list[dict] con id, nombre, version, descripcion, archivo
      acceso_archivos:
        • *
    ids:
      descripcion: Ids de todos los skills válidos de CE.
      entrada: *
      validar_esquema:
        • *
      salida: list[str]
      acceso_archivos:
        • *
    por_id:
      descripcion: Resuelve un skill por id.
      entrada: *
      validar_esquema:
        • *
      salida: dict del skill o None
      acceso_archivos:
        • *
    listar_archivos:
      descripcion: Nombres de *.py del directorio CE (implementación física de los skills).
      entrada: *
      validar_esquema:
        • *
      salida: list[str]
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Comprueba forma mínima de una salida de CE.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre CE. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de CE. Expone constantes, capacidades, skills y estado sin alterar el contrato ni ejecutar skills.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de CE como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    reporte:
      descripcion: Reporte de estado de CE: coherencia del inventario de skills, ids, archivos y capacidades declaradas.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con estado, coherente, ids, n, archivos, capacidades, operaciones_arquitectonicas
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnostico de problemas y recomendaciones sobre el inventario operativo de skills de CE.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones, coherente, ids, archivos
      acceso_archivos:
        • *
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • CE es una capacidad estructural; los skills son competencias operativas
    • Engine es la única autoridad que ejecuta los skills expuestos por CE
    • CE únicamente descubre, valida y expone skills
    • CE no toma decisiones ni selecciona skills
    • CE no coordina ciclos ni interpreta peticiones
    • las capacidades declaradas son callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
    • este módulo siempre puede reportar su propio estado
    • CE debe figurar en ROLES de core/engine.py
    • inventario() siempre incluye id, nombre, rol, version del CONTENEDOR
  reporte:
    id: CE
    modulo: capacidades_engine
    rol: CE
    version: 1.2
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    ids:
      • ce_mandato_catalogo
    n: 1
    archivos:
      • mandatos_ce.py
    errores:
      []
    errores_n: 0
    choques:
      []
    notas:
      []
    capacidades:
      • verificar
      • barrer
      • inventario
      • skills
      • ids
      • por_id
      • listar_archivos
      • verificar_salida
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • reporte
      • diagnostico
      • evaluar_universal
    capacidades_meta:
      • verificar
      • barrer
      • inventario
      • skills
      • ids
      • por_id
      • listar_archivos
      • verificar_salida
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • reporte
      • diagnostico
      • evaluar_universal
    autoridad:
      • Mantener el inventario operativo de skills nativos del Engine
      • Descubrir y validar forma mínima de cada skill
      • Exponer ids y skills a Engine
      • Reportar estado e inventario propios
    conocimiento_exportable:
      • skills
      • ids
      • por_id
      • listar_archivos
      • inventario
      • barrer
      • verificar
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
    operaciones_arquitectonicas:
      ejecutar_total: True
      inspeccionar: True
      registrar_inventario: True
  diagnostico:
    id: CE
    modulo: capacidades_engine
    rol: CE
    version: 1.2
    version_contrato: 1.0
    estado: OPERATIVO
    coherente: True
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    ids:
      • ce_mandato_catalogo
    n: 1
    archivos:
      • mandatos_ce.py
    errores:
      []
  inventario:
    id: CE
    nombre: capacidades_engine
    contenedor: capacidades_engine
    rol: CE
    version: 1.2
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    compatible_desde: 1.0
    api_engine: >=1.0
    ids:
      • ce_mandato_catalogo
    n: 1
    archivos:
      • mandatos_ce.py
    archivos_validos:
      • mandatos_ce.py
    archivos_sin_skill:
      []
    coherente: True
    errores:
      []
    choques:
      []
    notas:
      []
    skills:
      [0]
        id: ce_mandato_catalogo
        nombre: Mandato: consultar catalogo TT
        version: 1.0
        descripcion: Mandato del Engine: descubrir las escalas de verdad declaradas en el catalogo TT (y registrables en CA). CE no calcula ni inventa escalas.
        archivo: mandatos_ce.py
        oficio: NO ENTREGADO POR ENGINE
        material: NO ENTREGADO POR ENGINE
        valido: True
    capacidades:
      • barrer
      • diagnostico
      • ejecutar_total
      • evaluar_universal
      • ids
      • inspeccionar
      • inventario
      • listar_archivos
      • por_id
      • registrar_inventario
      • reporte
      • skills
      • verificar
      • verificar_salida
    capacidades_meta:
      • barrer
      • diagnostico
      • ejecutar_total
      • evaluar_universal
      • ids
      • inspeccionar
      • inventario
      • listar_archivos
      • por_id
      • registrar_inventario
      • reporte
      • skills
      • verificar
      • verificar_salida
    capacidades_callable:
      • barrer
      • diagnostico
      • ejecutar_total
      • evaluar_universal
      • ids
      • inspeccionar
      • inventario
      • listar_archivos
      • por_id
      • registrar_inventario
      • reporte
      • skills
      • verificar
      • verificar_salida
    n_capacidades: 14
    n_capacidades_meta: 14
    n_capacidades_callable: 14
    funcion: Capacidad estructural del Engine. Mantiene el inventario operativo de skills nativos. Cada archivo implementa uno o más skills. Engine es la única autoridad que los ejecuta. CE no calcula, no deposita, no decide, no selecciona.

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
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  consultas_soportadas:
    • listar_ids
    • consultar_por_id
    • obtener_esquema
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • verificar_coherencia
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • TT
    • SC
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
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
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia del glosario.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, categorias, ids, errores
      acceso_archivos:
        • *
    barrer:
      descripcion: Evalúa coherencia del glosario de IDs. No calcula.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, categorias, ids, errores, esquema
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario completo del módulo y de los IDs.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, version, categorias, ids, total, errores
      acceso_archivos:
        • *
    categorias:
      descripcion: Lista del catálogo si coherente; si no, lista vacía.
      entrada: *
      validar_esquema:
        • *
      salida: list[dict] de categorías normalizadas
      acceso_archivos:
        • *
    por_id:
      descripcion: Devuelve la categoría normalizada de un id, o None.
      entrada: *
      validar_esquema:
        • *
      salida: dict | None
      acceso_archivos:
        • *
    ids:
      descripcion: Lista de todos los ids del catálogo coherente.
      entrada: *
      validar_esquema:
        • *
      salida: list[str]
      acceso_archivos:
        • *
    esquema:
      descripcion: Esquema de forma de una categoría (obligatorios, opcionales, prohibidos).
      entrada: *
      validar_esquema:
        • *
      salida: dict ESQUEMA_CATEGORIA
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte interno de estado del módulo CC.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, coherente, categorias, ids, errores
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico: qué falta o está mal en el glosario.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Comprueba forma de una salida de barrer: coherente bool, errores list, ids list, categorias int.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre CC. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de CC. Expone constantes, capacidades, catálogo y estado sin alterar el contrato ni calcular.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de CC como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
    categorias: 214
    ids:
      • afirmaciones
      • afirmaciones_falsas
      • alpha
      • aplicar_escala
      • autoriza_engine
      • ax
      • barrer
      • base_nula
      • base_nula_c
      • base_nula_k
      • base_nula_l
      • beta
      • c
      • ca
      • calcular_c
      • calcular_k
      • calcular_l
      • calculator
      • capacidades
      • capacidades_meta
      • catalogo_citaciones
      • categorias
      • cc
      • coherencia
      • coherencia_fn
      • combinar_resultados
      • compromisos
      • conocimiento_exportable
      • contenedor
      • conteos
      • contexto
      • contradicciones
      • correlacion_fn
      • correlacion_k
      • ct
      • cx
      • decimal
      • degradado
      • denominador
      • descubrir
      • dg
      • diagnostico
      • display
      • ejecutar_capacidad
      • en
      • engine
      • es_valida
      • escala
      • escalas_ids
      • esquema
      • esquema_categoria
      • estados_validos
      • extraer_conteos
      • f
      • fo
      • formulas
      • fraccion
      • ids
      • invariantes
      • inventario
      • inyectar_en_peticion
      • k
      • l
      • leer_ids_escala
      • logica
      • logica_fn
      • m
      • mc
      • no_iniciado
      • numerador
      • o_context
      • o_presente
      • omega
      • omegareport
      • operativo
      • p
      • por_id
      • posturas
      • precision
      • r
      • rechazado
      • recolectar
      • reporte
      • reporting
      • representar
      • requiere
      • resolver_dependencias
      • resolver_pedido
      • reversiones
      • tru_atomo
      • tru_conversacion
      • tru_frase
      • tru_repositorio
      • tru_ri
      • tru_sujeto
      • tru_total
      • tru_totales
      • truth
      • tt
      • undefined
      • valor
      • verificar
      • verificar_c
      • verificar_escala
      • verificar_k
      • verificar_l
      • verificar_salida
      • afirmaciones
      • afirmaciones_falsas
      • alpha
      • aplicar_escala
      • autoriza_engine
      • ax
      • barrer
      • base_nula
      • base_nula_c
      • base_nula_k
      • base_nula_l
      • beta
      • c
      • ca
      • calcular_c
      • calcular_k
      • calcular_l
      • calculator
      • capacidades
      • capacidades_meta
      • catalogo_citaciones
      • categorias
      • cc
      • coherencia
      • coherencia_fn
      • combinar_resultados
      • compromisos
      • conocimiento_exportable
      • contenedor
      • conteos
      • contexto
      • contradicciones
      • correlacion_fn
      • correlacion_k
      • ct
      • cx
      • decimal
      • degradado
      • denominador
      • descubrir
      • dg
      • diagnostico
      • display
      • ejecutar_capacidad
      • en
      • engine
      • es_valida
      • escala
      • escalas_ids
      • esquema
      • esquema_categoria
      • estados_validos
      • extraer_conteos
      • f
      • fo
      • formulas
      • fraccion
      • ids
      • invariantes
      • inventario
      • inyectar_en_peticion
      • k
      • l
      • leer_ids_escala
      • logica
      • logica_fn
      • m
      • mc
      • no_iniciado
      • numerador
      • o_context
      • o_presente
      • omega
      • omegareport
      • operativo
      • p
      • por_id
      • posturas
      • precision
      • r
      • rechazado
      • recolectar
      • reporte
      • reporting
      • representar
      • requiere
      • resolver_dependencias
      • resolver_pedido
      • reversiones
      • tru_atomo
      • tru_conversacion
      • tru_frase
      • tru_repositorio
      • tru_ri
      • tru_sujeto
      • tru_total
      • tru_totales
      • truth
      • tt
      • undefined
      • valor
      • verificar
      • verificar_c
      • verificar_escala
      • verificar_k
      • verificar_l
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
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_ri' en ['ids_sistema', 'ids_sistema']
      [35]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_total' en ['ids_sistema', 'ids_sistema']
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
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'c' en ['ids_sistema', 'ids_sistema']
      [56]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'l' en ['ids_sistema', 'ids_sistema']
      [57]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'k' en ['ids_sistema', 'ids_sistema']
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
    errores_n: 107
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • TT
      • SC
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
    consultas_soportadas:
      • listar_ids
      • consultar_por_id
      • obtener_esquema
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • verificar_coherencia
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
    operaciones_arquitectonicas:
      ejecutar_total: True
      inspeccionar: True
      registrar_inventario: True
  diagnostico:
    id: CC
    modulo: catalogo_citaciones
    rol: CC
    version: 2.1
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estado: DEGRADADO
    coherente: False
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
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'tru_ri' en ['ids_sistema', 'ids_sistema']
          [35]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'tru_total' en ['ids_sistema', 'ids_sistema']
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
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'c' en ['ids_sistema', 'ids_sistema']
          [56]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'l' en ['ids_sistema', 'ids_sistema']
          [57]
            archivo: ids_sistema,ids_sistema
            error: id duplicado 'k' en ['ids_sistema', 'ids_sistema']
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
      • Corregir los archivos de categorias/ que presenten errores de carga, estructura o duplicidad.
    errores_n: 107
    categorias_n: 214
    ids_n: 214
    ids:
      • afirmaciones
      • afirmaciones_falsas
      • alpha
      • aplicar_escala
      • autoriza_engine
      • ax
      • barrer
      • base_nula
      • base_nula_c
      • base_nula_k
      • base_nula_l
      • beta
      • c
      • ca
      • calcular_c
      • calcular_k
      • calcular_l
      • calculator
      • capacidades
      • capacidades_meta
      • catalogo_citaciones
      • categorias
      • cc
      • coherencia
      • coherencia_fn
      • combinar_resultados
      • compromisos
      • conocimiento_exportable
      • contenedor
      • conteos
      • contexto
      • contradicciones
      • correlacion_fn
      • correlacion_k
      • ct
      • cx
      • decimal
      • degradado
      • denominador
      • descubrir
      • dg
      • diagnostico
      • display
      • ejecutar_capacidad
      • en
      • engine
      • es_valida
      • escala
      • escalas_ids
      • esquema
      • esquema_categoria
      • estados_validos
      • extraer_conteos
      • f
      • fo
      • formulas
      • fraccion
      • ids
      • invariantes
      • inventario
      • inyectar_en_peticion
      • k
      • l
      • leer_ids_escala
      • logica
      • logica_fn
      • m
      • mc
      • no_iniciado
      • numerador
      • o_context
      • o_presente
      • omega
      • omegareport
      • operativo
      • p
      • por_id
      • posturas
      • precision
      • r
      • rechazado
      • recolectar
      • reporte
      • reporting
      • representar
      • requiere
      • resolver_dependencias
      • resolver_pedido
      • reversiones
      • tru_atomo
      • tru_conversacion
      • tru_frase
      • tru_repositorio
      • tru_ri
      • tru_sujeto
      • tru_total
      • tru_totales
      • truth
      • tt
      • undefined
      • valor
      • verificar
      • verificar_c
      • verificar_escala
      • verificar_k
      • verificar_l
      • verificar_salida
      • afirmaciones
      • afirmaciones_falsas
      • alpha
      • aplicar_escala
      • autoriza_engine
      • ax
      • barrer
      • base_nula
      • base_nula_c
      • base_nula_k
      • base_nula_l
      • beta
      • c
      • ca
      • calcular_c
      • calcular_k
      • calcular_l
      • calculator
      • capacidades
      • capacidades_meta
      • catalogo_citaciones
      • categorias
      • cc
      • coherencia
      • coherencia_fn
      • combinar_resultados
      • compromisos
      • conocimiento_exportable
      • contenedor
      • conteos
      • contexto
      • contradicciones
      • correlacion_fn
      • correlacion_k
      • ct
      • cx
      • decimal
      • degradado
      • denominador
      • descubrir
      • dg
      • diagnostico
      • display
      • ejecutar_capacidad
      • en
      • engine
      • es_valida
      • escala
      • escalas_ids
      • esquema
      • esquema_categoria
      • estados_validos
      • extraer_conteos
      • f
      • fo
      • formulas
      • fraccion
      • ids
      • invariantes
      • inventario
      • inyectar_en_peticion
      • k
      • l
      • leer_ids_escala
      • logica
      • logica_fn
      • m
      • mc
      • no_iniciado
      • numerador
      • o_context
      • o_presente
      • omega
      • omegareport
      • operativo
      • p
      • por_id
      • posturas
      • precision
      • r
      • rechazado
      • recolectar
      • reporte
      • reporting
      • representar
      • requiere
      • resolver_dependencias
      • resolver_pedido
      • reversiones
      • tru_atomo
      • tru_conversacion
      • tru_frase
      • tru_repositorio
      • tru_ri
      • tru_sujeto
      • tru_total
      • tru_totales
      • truth
      • tt
      • undefined
      • valor
      • verificar
      • verificar_c
      • verificar_escala
      • verificar_k
      • verificar_l
      • verificar_salida
  inventario:
    id: CC
    nombre: catalogo_citaciones
    contenedor: catalogo_citaciones
    rol: CC
    version: 2.1
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: DEGRADADO
    coherente: False
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
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [1]
        id: afirmaciones_falsas
        nombre: afirmaciones_falsas
        unidad: clave
        enunciado: Clave de conteo: afirmaciones_falsas
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [2]
        id: alpha
        nombre: ALPHA
        unidad: factor
        enunciado: Factor o magnitud: ALPHA
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [3]
        id: aplicar_escala
        nombre: aplicar_escala
        unidad: funcion
        enunciado: Función o capacidad: aplicar_escala
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [4]
        id: autoriza_engine
        nombre: autoriza_engine
        unidad: campo
        enunciado: Campo estructural de contrato: autoriza_engine
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [5]
        id: ax
        nombre: AX
        unidad: rol
        enunciado: Módulo / rol del sistema: AX
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [6]
        id: barrer
        nombre: barrer
        unidad: funcion
        enunciado: Función o capacidad: barrer
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [7]
        id: base_nula
        nombre: base_nula
        unidad: meta
        enunciado: Metadato de dominio: base_nula
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [8]
        id: base_nula_c
        nombre: base_nula_C
        unidad: meta
        enunciado: Metadato de dominio: base_nula_C
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [9]
        id: base_nula_k
        nombre: base_nula_K
        unidad: meta
        enunciado: Metadato de dominio: base_nula_K
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [10]
        id: base_nula_l
        nombre: base_nula_L
        unidad: meta
        enunciado: Metadato de dominio: base_nula_L
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [11]
        id: beta
        nombre: BETA
        unidad: factor
        enunciado: Factor o magnitud: BETA
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [12]
        id: c
        nombre: C
        unidad: factor
        enunciado: Factor o magnitud: C
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [13]
        id: ca
        nombre: CA
        unidad: rol
        enunciado: Módulo / rol del sistema: CA
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [14]
        id: calcular_c
        nombre: calcular_c
        unidad: funcion
        enunciado: Función o capacidad: calcular_c
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [15]
        id: calcular_k
        nombre: calcular_k
        unidad: funcion
        enunciado: Función o capacidad: calcular_k
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [16]
        id: calcular_l
        nombre: calcular_l
        unidad: funcion
        enunciado: Función o capacidad: calcular_l
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [17]
        id: calculator
        nombre: calculator
        unidad: archivo
        enunciado: Archivo del repositorio: calculator
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [18]
        id: capacidades
        nombre: capacidades
        unidad: campo
        enunciado: Campo estructural de contrato: capacidades
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [19]
        id: capacidades_meta
        nombre: capacidades_meta
        unidad: campo
        enunciado: Campo estructural de contrato: capacidades_meta
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [20]
        id: catalogo_citaciones
        nombre: catalogo_citaciones
        unidad: archivo
        enunciado: Archivo del repositorio: catalogo_citaciones
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [21]
        id: categorias
        nombre: categorias
        unidad: funcion
        enunciado: Función o capacidad: categorias
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [22]
        id: cc
        nombre: CC
        unidad: rol
        enunciado: Módulo / rol del sistema: CC
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [23]
        id: coherencia
        nombre: coherencia
        unidad: archivo
        enunciado: Archivo del repositorio: coherencia
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [24]
        id: coherencia_fn
        nombre: coherencia_fn
        unidad: funcion
        enunciado: Función o capacidad: coherencia_fn
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [25]
        id: combinar_resultados
        nombre: combinar_resultados
        unidad: funcion
        enunciado: Función o capacidad: combinar_resultados
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [26]
        id: compromisos
        nombre: compromisos
        unidad: clave
        enunciado: Clave de conteo: compromisos
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [27]
        id: conocimiento_exportable
        nombre: conocimiento_exportable
        unidad: campo
        enunciado: Campo estructural de contrato: conocimiento_exportable
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [28]
        id: contenedor
        nombre: CONTENEDOR
        unidad: campo
        enunciado: Campo estructural de contrato: CONTENEDOR
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [29]
        id: conteos
        nombre: conteos
        unidad: archivo
        enunciado: Archivo del repositorio: conteos
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [30]
        id: contexto
        nombre: contexto
        unidad: meta
        enunciado: Metadato de dominio: contexto
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [31]
        id: contradicciones
        nombre: contradicciones
        unidad: clave
        enunciado: Clave de conteo: contradicciones
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [32]
        id: correlacion_fn
        nombre: correlacion_fn
        unidad: funcion
        enunciado: Función o capacidad: correlacion_fn
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [33]
        id: correlacion_k
        nombre: correlacion_k
        unidad: archivo
        enunciado: Archivo del repositorio: correlacion_k
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [34]
        id: ct
        nombre: CT
        unidad: rol
        enunciado: Módulo / rol del sistema: CT
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [35]
        id: cx
        nombre: CX
        unidad: rol
        enunciado: Módulo / rol del sistema: CX
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [36]
        id: decimal
        nombre: decimal
        unidad: campo
        enunciado: Campo de representación: decimal
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [37]
        id: degradado
        nombre: DEGRADADO
        unidad: estado
        enunciado: Estado de módulo: DEGRADADO
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=estado
      [38]
        id: denominador
        nombre: denominador
        unidad: campo
        enunciado: Campo de representación: denominador
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [39]
        id: descubrir
        nombre: descubrir
        unidad: funcion
        enunciado: Función o capacidad: descubrir
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [40]
        id: dg
        nombre: DG
        unidad: rol
        enunciado: Módulo / rol del sistema: DG
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [41]
        id: diagnostico
        nombre: diagnostico
        unidad: funcion
        enunciado: Función o capacidad: diagnostico
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [42]
        id: display
        nombre: display
        unidad: campo
        enunciado: Campo de representación: display
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [43]
        id: ejecutar_capacidad
        nombre: ejecutar_capacidad
        unidad: funcion
        enunciado: Función o capacidad: ejecutar_capacidad
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [44]
        id: en
        nombre: EN
        unidad: rol
        enunciado: Módulo / rol del sistema: EN
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [45]
        id: engine
        nombre: Engine
        unidad: agente
        enunciado: Agente del sistema: Engine
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=agente
      [46]
        id: es_valida
        nombre: es_valida
        unidad: funcion
        enunciado: Función o capacidad: es_valida
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [47]
        id: escala
        nombre: escala
        unidad: archivo
        enunciado: Archivo del repositorio: escala
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [48]
        id: escalas_ids
        nombre: escalas_ids
        unidad: archivo
        enunciado: Archivo del repositorio: escalas_ids
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [49]
        id: esquema
        nombre: esquema
        unidad: funcion
        enunciado: Función o capacidad: esquema
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [50]
        id: esquema_categoria
        nombre: ESQUEMA_CATEGORIA
        unidad: campo
        enunciado: Campo estructural de contrato: ESQUEMA_CATEGORIA
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [51]
        id: estados_validos
        nombre: estados_validos
        unidad: campo
        enunciado: Campo estructural de contrato: estados_validos
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [52]
        id: extraer_conteos
        nombre: extraer_conteos
        unidad: funcion
        enunciado: Función o capacidad: extraer_conteos
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [53]
        id: f
        nombre: f
        unidad: variable
        enunciado: Variable matemática: f
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=variable
      [54]
        id: fo
        nombre: FO
        unidad: rol
        enunciado: Módulo / rol del sistema: FO
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [55]
        id: formulas
        nombre: formulas
        unidad: archivo
        enunciado: Archivo del repositorio: formulas
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [56]
        id: fraccion
        nombre: fraccion
        unidad: campo
        enunciado: Campo de representación: fraccion
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [57]
        id: ids
        nombre: ids
        unidad: funcion
        enunciado: Función o capacidad: ids
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [58]
        id: invariantes
        nombre: invariantes
        unidad: campo
        enunciado: Campo estructural de contrato: invariantes
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [59]
        id: inventario
        nombre: inventario
        unidad: funcion
        enunciado: Función o capacidad: inventario
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [60]
        id: inyectar_en_peticion
        nombre: inyectar_en_peticion
        unidad: funcion
        enunciado: Función o capacidad: inyectar_en_peticion
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [61]
        id: k
        nombre: K
        unidad: factor
        enunciado: Factor o magnitud: K
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [62]
        id: l
        nombre: L
        unidad: factor
        enunciado: Factor o magnitud: L
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=factor
      [63]
        id: leer_ids_escala
        nombre: leer_ids_escala
        unidad: funcion
        enunciado: Función o capacidad: leer_ids_escala
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [64]
        id: logica
        nombre: logica
        unidad: archivo
        enunciado: Archivo del repositorio: logica
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [65]
        id: logica_fn
        nombre: logica_fn
        unidad: funcion
        enunciado: Función o capacidad: logica_fn
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [66]
        id: m
        nombre: m
        unidad: variable
        enunciado: Variable matemática: m
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=variable
      [67]
        id: mc
        nombre: MC
        unidad: rol
        enunciado: Módulo / rol del sistema: MC
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [68]
        id: no_iniciado
        nombre: NO_INICIADO
        unidad: estado
        enunciado: Estado de módulo: NO_INICIADO
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=estado
      [69]
        id: numerador
        nombre: numerador
        unidad: campo
        enunciado: Campo de representación: numerador
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [70]
        id: o_context
        nombre: O_context
        unidad: meta
        enunciado: Metadato de dominio: O_context
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [71]
        id: o_presente
        nombre: o_presente
        unidad: meta
        enunciado: Metadato de dominio: o_presente
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [72]
        id: omega
        nombre: Omega
        unidad: agente
        enunciado: Agente del sistema: Omega
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=agente
      [73]
        id: omegareport
        nombre: OmegaReport
        unidad: agente
        enunciado: Agente del sistema: OmegaReport
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=agente
      [74]
        id: operativo
        nombre: OPERATIVO
        unidad: estado
        enunciado: Estado de módulo: OPERATIVO
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=estado
      [75]
        id: p
        nombre: p
        unidad: variable
        enunciado: Variable matemática: p
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=variable
      [76]
        id: por_id
        nombre: por_id
        unidad: funcion
        enunciado: Función o capacidad: por_id
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [77]
        id: posturas
        nombre: posturas
        unidad: clave
        enunciado: Clave de conteo: posturas
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [78]
        id: precision
        nombre: precision
        unidad: campo
        enunciado: Campo de representación: precision
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [79]
        id: r
        nombre: r
        unidad: variable
        enunciado: Variable matemática: r
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=variable
      [80]
        id: rechazado
        nombre: RECHAZADO
        unidad: estado
        enunciado: Estado de módulo: RECHAZADO
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=estado
      [81]
        id: recolectar
        nombre: recolectar
        unidad: funcion
        enunciado: Función o capacidad: recolectar
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [82]
        id: reporte
        nombre: reporte
        unidad: funcion
        enunciado: Función o capacidad: reporte
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [83]
        id: reporting
        nombre: reporting
        unidad: campo
        enunciado: Campo estructural de contrato: reporting
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [84]
        id: representar
        nombre: representar
        unidad: funcion
        enunciado: Función o capacidad: representar
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [85]
        id: requiere
        nombre: requiere
        unidad: campo
        enunciado: Campo estructural de contrato: requiere
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=contrato
      [86]
        id: resolver_dependencias
        nombre: resolver_dependencias
        unidad: funcion
        enunciado: Función o capacidad: resolver_dependencias
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [87]
        id: resolver_pedido
        nombre: resolver_pedido
        unidad: funcion
        enunciado: Función o capacidad: resolver_pedido
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [88]
        id: reversiones
        nombre: reversiones
        unidad: clave
        enunciado: Clave de conteo: reversiones
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=conteo
      [89]
        id: tru_atomo
        nombre: tru_atomo
        unidad: escala
        enunciado: Escala de alcance Tru: tru_atomo
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=escala
      [90]
        id: tru_conversacion
        nombre: tru_conversacion
        unidad: escala
        enunciado: Escala de alcance Tru: tru_conversacion
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=escala
      [91]
        id: tru_frase
        nombre: tru_frase
        unidad: escala
        enunciado: Escala de alcance Tru: tru_frase
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=escala
      [92]
        id: tru_repositorio
        nombre: tru_repositorio
        unidad: escala
        enunciado: Escala de alcance Tru: tru_repositorio
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=escala
      [93]
        id: tru_ri
        nombre: tru_ri
        unidad: funcion
        enunciado: Función o capacidad: tru_ri
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [94]
        id: tru_sujeto
        nombre: tru_sujeto
        unidad: escala
        enunciado: Escala de alcance Tru: tru_sujeto
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=escala
      [95]
        id: tru_total
        nombre: tru_total
        unidad: funcion
        enunciado: Función o capacidad: tru_total
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [96]
        id: tru_totales
        nombre: tru_totales
        unidad: archivo
        enunciado: Archivo del repositorio: tru_totales
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [97]
        id: truth
        nombre: truth
        unidad: archivo
        enunciado: Archivo del repositorio: truth
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=archivo
      [98]
        id: tt
        nombre: TT
        unidad: rol
        enunciado: Módulo / rol del sistema: TT
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=modulo
      [99]
        id: undefined
        nombre: UNDEFINED
        unidad: meta
        enunciado: Metadato de dominio: UNDEFINED
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=meta
      [100]
        id: valor
        nombre: valor
        unidad: campo
        enunciado: Campo de representación: valor
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=representacion
      [101]
        id: verificar
        nombre: verificar
        unidad: funcion
        enunciado: Función o capacidad: verificar
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [102]
        id: verificar_c
        nombre: verificar_c
        unidad: funcion
        enunciado: Función o capacidad: verificar_c
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [103]
        id: verificar_escala
        nombre: verificar_escala
        unidad: funcion
        enunciado: Función o capacidad: verificar_escala
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [104]
        id: verificar_k
        nombre: verificar_k
        unidad: funcion
        enunciado: Función o capacidad: verificar_k
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [105]
        id: verificar_l
        nombre: verificar_l
        unidad: funcion
        enunciado: Función o capacidad: verificar_l
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [106]
        id: verificar_salida
        nombre: verificar_salida
        unidad: funcion
        enunciado: Función o capacidad: verificar_salida
        nivel_fractal: 1
        jurisdiccion: SISTEMA
        requiere:
          []
        factores_evaluables:
          []
        agrega_desde:
          []
        fuente_modulo: CC
        senales:
          []
        anclas:
          []
        origen: ids_sistema
        version: 1.0
        notas: clase=funcion
      [107]
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
      [108]
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
      [109]
        id: alpha
        nombre: alpha
        unidad: id
        enunciado: ID del repositorio: alpha
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
      [111]
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
      [112]
        id: ax
        nombre: ax
        unidad: id
        enunciado: ID del repositorio: ax
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
      [113]
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
      [114]
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
      [115]
        id: base_nula_c
        nombre: base_nula_c
        unidad: id
        enunciado: ID del repositorio: base_nula_c
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
        id: base_nula_k
        nombre: base_nula_k
        unidad: id
        enunciado: ID del repositorio: base_nula_k
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
      [117]
        id: base_nula_l
        nombre: base_nula_l
        unidad: id
        enunciado: ID del repositorio: base_nula_l
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
        id: beta
        nombre: beta
        unidad: id
        enunciado: ID del repositorio: beta
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
      [119]
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
      [120]
        id: ca
        nombre: ca
        unidad: id
        enunciado: ID del repositorio: ca
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
      [121]
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
      [122]
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
      [123]
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
      [124]
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
      [125]
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
      [126]
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
      [127]
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
      [128]
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
      [129]
        id: cc
        nombre: cc
        unidad: id
        enunciado: ID del repositorio: cc
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
      [131]
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
      [132]
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
      [133]
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
      [134]
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
      [135]
        id: contenedor
        nombre: contenedor
        unidad: id
        enunciado: ID del repositorio: contenedor
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
      [137]
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
      [138]
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
      [139]
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
      [140]
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
      [141]
        id: ct
        nombre: ct
        unidad: id
        enunciado: ID del repositorio: ct
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
        id: cx
        nombre: cx
        unidad: id
        enunciado: ID del repositorio: cx
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
      [143]
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
      [144]
        id: degradado
        nombre: degradado
        unidad: id
        enunciado: ID del repositorio: degradado
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
      [145]
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
      [146]
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
      [147]
        id: dg
        nombre: dg
        unidad: id
        enunciado: ID del repositorio: dg
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
      [149]
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
      [150]
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
      [151]
        id: en
        nombre: en
        unidad: id
        enunciado: ID del repositorio: en
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
        id: engine
        nombre: engine
        unidad: id
        enunciado: ID del repositorio: engine
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
      [153]
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
      [154]
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
      [155]
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
      [156]
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
      [157]
        id: esquema_categoria
        nombre: esquema_categoria
        unidad: id
        enunciado: ID del repositorio: esquema_categoria
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
      [159]
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
      [160]
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
      [161]
        id: fo
        nombre: fo
        unidad: id
        enunciado: ID del repositorio: fo
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
      [163]
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
      [164]
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
      [165]
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
      [166]
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
      [167]
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
      [168]
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
      [169]
        id: l
        nombre: l
        unidad: id
        enunciado: ID del repositorio: l
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
      [171]
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
      [172]
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
      [173]
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
      [174]
        id: mc
        nombre: mc
        unidad: id
        enunciado: ID del repositorio: mc
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
      [175]
        id: no_iniciado
        nombre: no_iniciado
        unidad: id
        enunciado: ID del repositorio: no_iniciado
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
      [177]
        id: o_context
        nombre: o_context
        unidad: id
        enunciado: ID del repositorio: o_context
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
      [179]
        id: omega
        nombre: omega
        unidad: id
        enunciado: ID del repositorio: omega
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
        id: omegareport
        nombre: omegareport
        unidad: id
        enunciado: ID del repositorio: omegareport
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
      [181]
        id: operativo
        nombre: operativo
        unidad: id
        enunciado: ID del repositorio: operativo
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
      [183]
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
      [184]
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
      [185]
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
      [186]
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
      [187]
        id: rechazado
        nombre: rechazado
        unidad: id
        enunciado: ID del repositorio: rechazado
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
      [189]
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
      [190]
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
      [191]
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
      [192]
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
      [193]
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
      [194]
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
      [195]
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
      [196]
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
      [197]
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
      [198]
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
      [199]
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
      [200]
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
      [201]
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
      [202]
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
      [203]
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
      [204]
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
      [205]
        id: tt
        nombre: tt
        unidad: id
        enunciado: ID del repositorio: tt
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
        nombre: undefined
        unidad: id
        enunciado: ID del repositorio: undefined
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
      [207]
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
      [208]
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
      [209]
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
      [210]
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
      [211]
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
      [212]
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
      [213]
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
      • afirmaciones_falsas
      • alpha
      • aplicar_escala
      • autoriza_engine
      • ax
      • barrer
      • base_nula
      • base_nula_c
      • base_nula_k
      • base_nula_l
      • beta
      • c
      • ca
      • calcular_c
      • calcular_k
      • calcular_l
      • calculator
      • capacidades
      • capacidades_meta
      • catalogo_citaciones
      • categorias
      • cc
      • coherencia
      • coherencia_fn
      • combinar_resultados
      • compromisos
      • conocimiento_exportable
      • contenedor
      • conteos
      • contexto
      • contradicciones
      • correlacion_fn
      • correlacion_k
      • ct
      • cx
      • decimal
      • degradado
      • denominador
      • descubrir
      • dg
      • diagnostico
      • display
      • ejecutar_capacidad
      • en
      • engine
      • es_valida
      • escala
      • escalas_ids
      • esquema
      • esquema_categoria
      • estados_validos
      • extraer_conteos
      • f
      • fo
      • formulas
      • fraccion
      • ids
      • invariantes
      • inventario
      • inyectar_en_peticion
      • k
      • l
      • leer_ids_escala
      • logica
      • logica_fn
      • m
      • mc
      • no_iniciado
      • numerador
      • o_context
      • o_presente
      • omega
      • omegareport
      • operativo
      • p
      • por_id
      • posturas
      • precision
      • r
      • rechazado
      • recolectar
      • reporte
      • reporting
      • representar
      • requiere
      • resolver_dependencias
      • resolver_pedido
      • reversiones
      • tru_atomo
      • tru_conversacion
      • tru_frase
      • tru_repositorio
      • tru_ri
      • tru_sujeto
      • tru_total
      • tru_totales
      • truth
      • tt
      • undefined
      • valor
      • verificar
      • verificar_c
      • verificar_escala
      • verificar_k
      • verificar_l
      • verificar_salida
      • afirmaciones
      • afirmaciones_falsas
      • alpha
      • aplicar_escala
      • autoriza_engine
      • ax
      • barrer
      • base_nula
      • base_nula_c
      • base_nula_k
      • base_nula_l
      • beta
      • c
      • ca
      • calcular_c
      • calcular_k
      • calcular_l
      • calculator
      • capacidades
      • capacidades_meta
      • catalogo_citaciones
      • categorias
      • cc
      • coherencia
      • coherencia_fn
      • combinar_resultados
      • compromisos
      • conocimiento_exportable
      • contenedor
      • conteos
      • contexto
      • contradicciones
      • correlacion_fn
      • correlacion_k
      • ct
      • cx
      • decimal
      • degradado
      • denominador
      • descubrir
      • dg
      • diagnostico
      • display
      • ejecutar_capacidad
      • en
      • engine
      • es_valida
      • escala
      • escalas_ids
      • esquema
      • esquema_categoria
      • estados_validos
      • extraer_conteos
      • f
      • fo
      • formulas
      • fraccion
      • ids
      • invariantes
      • inventario
      • inyectar_en_peticion
      • k
      • l
      • leer_ids_escala
      • logica
      • logica_fn
      • m
      • mc
      • no_iniciado
      • numerador
      • o_context
      • o_presente
      • omega
      • omegareport
      • operativo
      • p
      • por_id
      • posturas
      • precision
      • r
      • rechazado
      • recolectar
      • reporte
      • reporting
      • representar
      • requiere
      • resolver_dependencias
      • resolver_pedido
      • reversiones
      • tru_atomo
      • tru_conversacion
      • tru_frase
      • tru_repositorio
      • tru_ri
      • tru_sujeto
      • tru_total
      • tru_totales
      • truth
      • tt
      • undefined
      • valor
      • verificar
      • verificar_c
      • verificar_escala
      • verificar_k
      • verificar_l
      • verificar_salida
    total: 214
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
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_ri' en ['ids_sistema', 'ids_sistema']
      [35]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'tru_total' en ['ids_sistema', 'ids_sistema']
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
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'c' en ['ids_sistema', 'ids_sistema']
      [56]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'l' en ['ids_sistema', 'ids_sistema']
      [57]
        archivo: ids_sistema,ids_sistema
        error: id duplicado 'k' en ['ids_sistema', 'ids_sistema']
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
    errores_n: 107
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • TT
      • SC
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
  MÓDULO CIT/citacion
══════════════════════════════════════════════════════════════════════
  id: CIT
  nombre: citacion
  rol: CIT
  version: 2.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Autoridad universal de fundamentación del VPSI. Conserva conocimiento resoluble de todas las declaraciones públicas del sistema. Puede resolver, relacionar y citar cualquier declaración formal proveniente de cualquier módulo presente o futuro. Autoridad absoluta sobre la fundamentación, la resolución, la citación, la cadena normativa y la explicación documental. No altera el conocimiento declarado.
  funcion: Resolver, organizar, relacionar y citar cualquier declaración pública perteneciente al VPSI. Modo Engine: cadena documental del ciclo. Modo Consulta: resolución y explicación bajo demanda.
  no_hace:
    • Ninguna capacidad de CIT puede modificar el conocimiento declarado
  autoridad:
    • Autoridad absoluta sobre la fundamentación
    • Autoridad absoluta sobre la resolución de declaraciones
    • Autoridad absoluta sobre la citación
    • Autoridad absoluta sobre la cadena normativa
    • Autoridad absoluta sobre la explicación documental de cualquier cálculo
    • Autoridad absoluta sobre la relación entre declaraciones
    • Autoridad absoluta para responder consultas sobre el conocimiento declarado
  conocimiento_exportable:
    • declaraciones
    • resolver
    • buscar
    • cadena
    • explicar
    • citar
    • anunciar
    • relacionar
    • inventario
    • reporte
    • diagnostico
  consultas_soportadas:
    • resolver
    • buscar
    • buscar_por_tipo
    • buscar_por_fuente
    • cadena
    • explicar
    • citar
    • anunciar
    • relacionar
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
  capacidades:
    • verificar
    • barrer
    • verificar_salida
    • inventario
    • reporte
    • diagnostico
    • anunciar
    • anunciar_todo
    • citar
    • registrar
    • resolver
    • resolver_enunciado
    • buscar
    • cadena
    • explicar
    • relacionar
    • limpiar_ciclo
    • evaluar
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Centinela del oficio de fundamentación.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, coherente, errores, choques
      acceso_archivos:
        • *
    barrer:
      descripcion: Alias de verificar.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, coherente, errores, choques
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario contractual de CIT.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, nombre, rol, version, capacidades, tipos_declaracion
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte de estado de CIT.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, estado, coherente, registro_n
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico propio de CIT.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, estado, problemas, advertencias
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Forma mínima de salida de CIT.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    anunciar:
      descripcion: Modo Engine (paquete) o Consulta (declaración). Fundamentación documental sin recálculo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con anuncios / cadena documental
      acceso_archivos:
        • *
    anunciar_todo:
      descripcion: Anuncia todas las declaraciones del registro operativo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con anuncios, n
      acceso_archivos:
        • *
    citar:
      descripcion: Representación citable de declaraciones.
      entrada: *
      validar_esquema:
        • *
      salida: dict con citas, n
      acceso_archivos:
        • *
    registrar:
      descripcion: Incorpora declaración al registro operativo. No altera origen.
      entrada: *
      validar_esquema:
        • *
      salida: dict con ok, declaracion
      acceso_archivos:
        • *
    resolver:
      descripcion: Resuelve una declaración por id.
      entrada: *
      validar_esquema:
        • *
      salida: dict con resuelto, declaracion
      acceso_archivos:
        • *
    resolver_enunciado:
      descripcion: Alias de resolución orientado a enunciado.
      entrada: *
      validar_esquema:
        • *
      salida: dict con resuelto, enunciado
      acceso_archivos:
        • *
    buscar:
      descripcion: Consulta declaraciones del registro operativo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con declaraciones, n
      acceso_archivos:
        • *
    cadena:
      descripcion: Construye cadena normativa a partir de ids resolubles.
      entrada: *
      validar_esquema:
        • *
      salida: dict con cadena, faltantes, completa
      acceso_archivos:
        • *
    explicar:
      descripcion: Explicación documental solo con declaraciones existentes.
      entrada: *
      validar_esquema:
        • *
      salida: dict con explicacion, n, completa
      acceso_archivos:
        • *
    relacionar:
      descripcion: Documenta relación entre dos declaraciones resolubles.
      entrada: *
      validar_esquema:
        • *
      salida: dict con ok, declaracion de enlace
      acceso_archivos:
        • *
    limpiar_ciclo:
      descripcion: Limpia registro operativo del ciclo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con ok, limpiadas
      acceso_archivos:
        • *
    evaluar:
      descripcion: Alias de anunciar (compatibilidad Engine).
      entrada: *
      validar_esquema:
        • *
      salida: dict de anuncio / fundamentación
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre CIT. Ejerce todas las unidades ejecutables. No inventa.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Inspeccion estructural de CIT sin alterar contrato.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura y estado
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Instantanea determinista del inventario de CIT.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • CIT conserva conocimiento declarativo universal resoluble
    • CIT puede resolver cualquier declaración registrada
    • CIT puede citar cualquier declaración registrada
    • CIT puede construir cadenas de fundamentación
    • CIT puede responder consultas documentales
    • CIT nunca altera el conocimiento declarado
    • CIT nunca modifica resultados
    • CIT nunca reemplaza la autoridad de otros módulos
    • CIT únicamente documenta y fundamenta
    • Toda explicación producida por CIT debe provenir de declaraciones existentes
    • Toda cita debe ser resoluble
    • Toda cadena normativa debe ser trazable
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • las capacidades declaradas son callables tras la resolución
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
    • este módulo siempre puede reportar su propio estado
    • inventario() siempre incluye id, nombre, rol, version
  reporte:
    id: CIT
    nombre: citacion
    rol: CIT
    version: 2.0
    estado: OPERATIVO
    coherente: True
    registro_n: 0
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • inventario
      • reporte
      • diagnostico
      • anunciar
      • anunciar_todo
      • citar
      • registrar
      • resolver
      • resolver_enunciado
      • buscar
      • cadena
      • explicar
      • relacionar
      • limpiar_ciclo
      • evaluar
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    nota: CIT documenta y fundamenta. No calcula. No altera declaraciones de origen.
  diagnostico:
    id: CIT
    nombre: citacion
    rol: CIT
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    coherente: True
    registro_n: 0
    nota: Diagnóstico propio de CIT. No consulta autoridades ajenas.
  inventario:
    id: CIT
    nombre: citacion
    rol: CIT
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    compatible_desde: 1.0
    api_engine: >=1.0
    tipos_declaracion:
      • axioma
      • teorema
      • definicion
      • corolario
      • lema
      • regla
      • principio
      • formula
      • correlacion
      • contexto
      • limite
      • factor
      • procedimiento
      • contrato
      • invariante
      • capacidad
      • evidencia
      • citacion
      • ax
      • mc
      • cx
      • tx
      • ca
      • fo
      • re
      • ct
      • ch
      • sf
    relaciones:
      • depende_de
      • fundamenta
      • contradice
      • extiende
      • deriva_de
      • correlaciona_con
      • limita
      • activa
      • desactiva
      • requiere
      • gobierna
    campos_obligatorios:
      • id
      • tipo
      • fuente
      • enunciado
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • inventario
      • reporte
      • diagnostico
      • anunciar
      • anunciar_todo
      • citar
      • registrar
      • resolver
      • resolver_enunciado
      • buscar
      • cadena
      • explicar
      • relacionar
      • limpiar_ciclo
      • evaluar
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    registro_n: 0
    funcion: Autoridad universal de fundamentación. Resuelve, organiza, relaciona y cita cualquier declaración pública del VPSI. No modifica conocimiento.
    modos:
      • engine
      • consulta
    requiere:
      []

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
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
    validar_esquema: True
    acceso_archivos: True
  capacidades:
    • alpha
    • beta
    • buscar_constante
    • descubrir_constantes
    • diagnostico
    • ejecutar_total
    • evaluar_universal
    • inspeccionar
    • inventario
    • listar_constantes
    • registrar_inventario
    • reporte
    • verificar
    • verificar_constantes
  capacidades_meta:
    alpha:
      descripcion: Devuelve la constante fundacional ALPHA = 26/27.
      entrada: *
      validar_esquema:
        • *
      salida: Fraction(26, 27)
      acceso_archivos:
        • *
    beta:
      descripcion: Devuelve la constante fundacional BETA = 1/27.
      entrada: *
      validar_esquema:
        • *
      salida: Fraction(1, 27)
      acceso_archivos:
        • *
    descubrir_constantes:
      descripcion: Descubre todas las constantes oficiales declaradas dentro del modulo.
      entrada: *
      validar_esquema:
        • *
      salida: dict nombre -> meta de constante + errores_carga + total
      acceso_archivos:
        • *
    listar_constantes:
      descripcion: Lista nombres de constantes fundacionales y auxiliares.
      entrada: *
      validar_esquema:
        • *
      salida: dict con fundacionales, auxiliares, total
      acceso_archivos:
        • *
    buscar_constante:
      descripcion: Busca una constante oficial por nombre.
      entrada: *
      validar_esquema:
        • *
      salida: dict de la constante o None
      acceso_archivos:
        • *
    verificar_constantes:
      descripcion: Audita el dominio de constantes: invariante fundacional, duplicados, tipos, campos obligatorios, conflictos y carga.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, problemas, advertencias, total_constantes
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario completo de constantes del modulo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con total, fundacionales, auxiliares, constantes descubiertas
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte interno de estado del modulo CT.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, ALPHA, BETA, total_constantes, capacidades
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnostico de coherencia del dominio de constantes.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    verificar:
      descripcion: Verifica la invariante fundacional ALPHA + BETA == 1.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, ALPHA, BETA, suma
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Ejecuta el conjunto completo de capacidades operativamente ejercibles por Engine sobre CT, respetando el contrato, las autorizaciones y las capacidades realmente declaradas.
      entrada: dict opcional de peticion
      validar_esquema:
        • *
      salida: dict con id, modulo, rol, version, operacion, estado, coherente, capacidades_ejecutadas, errores_ejecucion, resultados y capacidades_declaradas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Inspecciona estructuralmente CT y expone su contrato, capacidades, constantes, integridad, autorizaciones y estado sin modificar el conocimiento declarado.
      entrada: dict opcional de peticion
      validar_esquema:
        • *
      salida: dict con id, modulo, rol, version, operacion, constantes, capacidades_contractuales, capacidades_meta, integridad, esquema, autoriza_engine, reporting e invariantes
      acceso_archivos:
        • *
    registrar_inventario:
      descripcion: Registra una instantánea determinista del inventario estructural y contractual de CT sin modificar las constantes declaradas ni el contrato del modulo.
      entrada: dict opcional de peticion
      validar_esquema:
        • *
      salida: dict con id, operacion, registrado, inventario y nota
      acceso_archivos:
        • *
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
      • buscar_constante
      • descubrir_constantes
      • diagnostico
      • ejecutar_total
      • evaluar_universal
      • inspeccionar
      • inventario
      • listar_constantes
      • registrar_inventario
      • reporte
      • verificar
      • verificar_constantes
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
  diagnostico:
    id: CT
    modulo: constante
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      • Dominio de constantes coherente.
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
      • buscar_constante
      • descubrir_constantes
      • diagnostico
      • ejecutar_total
      • evaluar_universal
      • inspeccionar
      • inventario
      • listar_constantes
      • registrar_inventario
      • reporte
      • verificar
      • verificar_constantes
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
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
  MÓDULO CX/contexto
══════════════════════════════════════════════════════════════════════
  id: CX
  nombre: contexto
  rol: CX
  version: 2.3
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Representación operativa del marco evaluable O_context.
  funcion: Generar el marco O a partir de la petición y garantizar la coherencia estructural de su dominio.
  no_hace:
    • No calcula valores de verdad
    • No asigna magnitudes numéricas de correlación
    • No importa código ajeno a su directorio
    • No declara dependencias de dominio
    • No orquesta ciclos
    • No emite cadenas auditables
  autoridad:
    • Declarar el registro O y permite_k
    • Clasificar el contexto evaluable
    • Validar la estructura y el dominio de los archivos internos
    • Reportar el estado estructural del módulo
    • Declarar la política de inventario y ejecución del módulo
    • Registrar todos los componentes descubiertos
    • Determinar qué componentes son operacionalmente ejecutables conforme al contrato
    • Ejercer la ejecución total solicitada por Engine
  conocimiento_exportable:
    • O_context
    • registro
    • permite_k
    • pedir_anuncio
    • tipos_peticion
    • inventario
    • inventario_total
    • componentes
    • unidades_ejecutables
    • ejecucion
    • reporte
    • diagnostico
    • axiomas
  consultas_soportadas:
    • resolver
    • centinela
    • inventario
    • reporte
    • diagnostico
    • verificar
    • axiomas
    • ejecutar
    • ejecutar_total
    • registrar_inventario
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    evaluar_universal: True
  capacidades:
    • resolver
    • evaluar
    • centinela
    • verificar
    • barrer
    • inventario
    • reporte
    • diagnostico
    • axiomas
    • verificar_salida
    • ejecutar
    • ejecutar_total
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    resolver:
      descripcion: Garantiza el marco O clasificado a partir de la petición.
      entrada: *
      validar_esquema:
        • *
      salida: dict con O_context, registro, permite_k, coherente, errores
      acceso_archivos:
        • *
    evaluar:
      descripcion: Alias de resolver.
      entrada: *
      validar_esquema:
        • *
      salida: dict con O_context, registro, permite_k, coherente
      acceso_archivos:
        • *
    centinela:
      descripcion: Garantiza la coherencia estructural del dominio.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, total, choques, detalle, errores
      acceso_archivos:
        • *
    verificar:
      descripcion: Alias de barrer.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, errores, reglas_internas
      acceso_archivos:
        • *
    barrer:
      descripcion: Garantiza la coherencia de los clasificadores internos.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, errores, reglas_internas
      acceso_archivos:
        • *
    inventario:
      descripcion: Garantiza la enumeración de lo que existe en el módulo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, version, reglas_internas, modos, estados, capacidades, inventario_total
      acceso_archivos:
        • *
    reporte:
      descripcion: Garantiza el estado actual del módulo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, coherente, version, reglas_n
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Garantiza problemas, advertencias y recomendaciones.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    axiomas:
      descripcion: Garantiza las declaraciones operativas del dominio.
      entrada: *
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Garantiza la validez estructural de una salida del módulo.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    ejecutar:
      descripcion: Ejercer todas las unidades operativas ejecutables descubiertas dentro del módulo conforme al contrato y a sus leyes internas.
      entrada: *
      validar_esquema:
        • *
      salida: dict con inventario, ejecuciones, resultados, errores, advertencias y estado
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Alias contractual de ejecutar.
      entrada: *
      validar_esquema:
        • *
      salida: dict con inventario, ejecuciones, resultados, errores, advertencias y estado
      acceso_archivos:
        • *
    registrar_inventario:
      descripcion: Construir el inventario estructural completo del módulo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con archivos, componentes, funciones, clases, constantes, reglas, capacidades y unidades ejecutables
      acceso_archivos:
        • *
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
    • todo *.py interno se valida por estructura y dominio
    • permite_k exige registro con estado=estable, O_id y enunciado_O
    • pedir_anuncio verdadero implica tipos_peticion no vacío
    • el inventario total no omite componentes descubiertos del módulo
    • ejecutar no equivale a resolver
    • ejecutar total ejerce todas las unidades operativamente ejecutables
    • todo componente descubierto recibe clasificación estructural
    • ningún componente descubierto se convierte en ejecutable arbitrariamente
    • todo componente ejecutable posee una estrategia de ejecución válida
  reporte:
    id: CX
    modulo: contexto
    rol: CX
    dominio: CX
    version: 2.3
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    reglas_n: 8
    capacidades:
      • resolver
      • evaluar
      • centinela
      • verificar
      • barrer
      • inventario
      • reporte
      • diagnostico
      • axiomas
      • verificar_salida
      • ejecutar
      • ejecutar_total
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    autoridad:
      • Declarar el registro O y permite_k
      • Clasificar el contexto evaluable
      • Validar la estructura y el dominio de los archivos internos
      • Reportar el estado estructural del módulo
      • Declarar la política de inventario y ejecución del módulo
      • Registrar todos los componentes descubiertos
      • Determinar qué componentes son operacionalmente ejecutables conforme al contrato
      • Ejercer la ejecución total solicitada por Engine
    conocimiento_exportable:
      • O_context
      • registro
      • permite_k
      • pedir_anuncio
      • tipos_peticion
      • inventario
      • inventario_total
      • componentes
      • unidades_ejecutables
      • ejecucion
      • reporte
      • diagnostico
      • axiomas
    consultas_soportadas:
      • resolver
      • centinela
      • inventario
      • reporte
      • diagnostico
      • verificar
      • axiomas
      • ejecutar
      • ejecutar_total
      • registrar_inventario
  diagnostico:
    id: CX
    modulo: contexto
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    coherente: True
    errores_n: 0
    reglas_n: 8
  inventario:
    id: CX
    nombre: contexto
    rol: CX
    dominio: CX
    version: 2.3
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    capacidades:
      • resolver
      • evaluar
      • centinela
      • verificar
      • barrer
      • inventario
      • reporte
      • diagnostico
      • axiomas
      • verificar_salida
      • ejecutar
      • ejecutar_total
      • registrar_inventario
      • evaluar_universal
    capacidades_declaradas:
      • resolver
      • evaluar
      • centinela
      • verificar
      • barrer
      • inventario
      • reporte
      • diagnostico
      • axiomas
      • verificar_salida
      • ejecutar
      • ejecutar_total
      • registrar_inventario
      • evaluar_universal
    capacidades_resueltas:
      • resolver
      • evaluar
      • centinela
      • verificar
      • barrer
      • inventario
      • reporte
      • diagnostico
      • axiomas
      • verificar_salida
      • ejecutar
      • ejecutar_total
      • registrar_inventario
      • evaluar_universal
    reglas_internas:
      • auto_auditoria
      • declaracion_O
      • entendimiento_fractal
      • entrada_natural
      • marco_desde_repositorio
      • nucleo_sm_CX
      • peticion_anuncio
      • secuencia_conversacion
    total_reglas: 8
    modos_entrada:
      • conversacion
      • afirmacion
      • teorema
      • auditoria
      • texto_libre
      • repositorio
    estados_O:
      • estable
      • cambio
      • indefinido
    eventos:
      • mismo_O
      • expansion
      • cambio
      • indefinido
    tipos_peticion:
      • por_que_valor
      • dame_O
      • dame_evidencia
      • dame_normas
      • dame_limites
      • dame_cadena_completa
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    autoridad:
      • Declarar el registro O y permite_k
      • Clasificar el contexto evaluable
      • Validar la estructura y el dominio de los archivos internos
      • Reportar el estado estructural del módulo
      • Declarar la política de inventario y ejecución del módulo
      • Registrar todos los componentes descubiertos
      • Determinar qué componentes son operacionalmente ejecutables conforme al contrato
      • Ejercer la ejecución total solicitada por Engine
    conocimiento_exportable:
      • O_context
      • registro
      • permite_k
      • pedir_anuncio
      • tipos_peticion
      • inventario
      • inventario_total
      • componentes
      • unidades_ejecutables
      • ejecucion
      • reporte
      • diagnostico
      • axiomas
    consultas_soportadas:
      • resolver
      • centinela
      • inventario
      • reporte
      • diagnostico
      • verificar
      • axiomas
      • ejecutar
      • ejecutar_total
      • registrar_inventario
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
      • todo *.py interno se valida por estructura y dominio
      • permite_k exige registro con estado=estable, O_id y enunciado_O
      • pedir_anuncio verdadero implica tipos_peticion no vacío
      • el inventario total no omite componentes descubiertos del módulo
      • ejecutar no equivale a resolver
      • ejecutar total ejerce todas las unidades operativamente ejecutables
      • todo componente descubierto recibe clasificación estructural
      • ningún componente descubierto se convierte en ejecutable arbitrariamente
      • todo componente ejecutable posee una estrategia de ejecución válida
    archivos:
      [0]
        nombre: __init__.py
        ruta: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/__init__.py
        tipo: archivo
        declarado: True
        descubierto: True
      [1]
        nombre: auto_auditoria.py
        ruta: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/auto_auditoria.py
        tipo: archivo
        declarado: False
        descubierto: True
      [2]
        nombre: declaracion_O.py
        ruta: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/declaracion_O.py
        tipo: archivo
        declarado: False
        descubierto: True
      [3]
        nombre: entendimiento_fractal.py
        ruta: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/entendimiento_fractal.py
        tipo: archivo
        declarado: False
        descubierto: True
      [4]
        nombre: entrada_natural.py
        ruta: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/entrada_natural.py
        tipo: archivo
        declarado: False
        descubierto: True
      [5]
        nombre: marco_desde_repositorio.py
        ruta: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/marco_desde_repositorio.py
        tipo: archivo
        declarado: False
        descubierto: True
      [6]
        nombre: nucleo_sm_CX.py
        ruta: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/nucleo_sm_CX.py
        tipo: archivo
        declarado: False
        descubierto: True
      [7]
        nombre: peticion_anuncio.py
        ruta: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/peticion_anuncio.py
        tipo: archivo
        declarado: False
        descubierto: True
      [8]
        nombre: secuencia_conversacion.py
        ruta: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/secuencia_conversacion.py
        tipo: archivo
        declarado: False
        descubierto: True
    componentes:
      [0]
        nombre: API_ENGINE
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: '>=1.0'
      [1]
        nombre: ARCHIVOS_PY
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: [PosixPath('/home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/__init__.py'), PosixPath('/home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/auto_auditoria.py'), PosixPath('
      [2]
        nombre: Any
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: clase
        estado: descubierto
        errores:
          []
      [3]
        nombre: CLAVES_FUERA_DE_DOMINIO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['Tru_Ri', 'Tru_total', 'tru_ri', 'tru_total', 'C', 'L', 'K', 'alpha', 'beta', 'ALPHA', 'BETA']
      [4]
        nombre: CLAVES_PEDIR_ANUNCIO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['pedir_anuncio', 'pedir_cita', 'anuncio', 'citar', 'cadena_auditable', 'dame_por_que']
      [5]
        nombre: COMPATIBLE_DESDE
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: '1.0'
      [6]
        nombre: CONTENEDOR
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: {'esquema': 'VPSI-CONTRACT-1.0', 'version_contrato': '1.0', 'version_modulo': '2.3', 'estabilidad': 'ESTABLE', 'compatible_desde': '1.0', 'api_engine': '>=1.0', 'id': 'CX', 'nombre': 'contexto', 'rol'
      [7]
        nombre: ContextoError
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: excepcion
        estado: descubierto
        errores:
          []
      [8]
        nombre: ContratoInvalido
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: excepcion
        estado: descubierto
        errores:
          []
      [9]
        nombre: ESQUEMA_CONTRATO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'VPSI-CONTRACT-1.0'
      [10]
        nombre: ESTABILIDAD
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'ESTABLE'
      [11]
        nombre: ESTADOS_O
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['estable', 'cambio', 'indefinido']
      [12]
        nombre: ESTADOS_VALIDOS
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ('NO_INICIADO', 'OPERATIVO', 'DEGRADADO', 'RECHAZADO')
      [13]
        nombre: ESTADO_DEGRADADO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'DEGRADADO'
      [14]
        nombre: ESTADO_NO_INICIADO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'NO_INICIADO'
      [15]
        nombre: ESTADO_OPERATIVO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'OPERATIVO'
      [16]
        nombre: ESTADO_RECHAZADO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'RECHAZADO'
      [17]
        nombre: EVENTOS
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['mismo_O', 'expansion', 'cambio', 'indefinido']
      [18]
        nombre: ID_MODULO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'CX'
      [19]
        nombre: INVARIANTES
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ('el id del módulo nunca cambia', 'el rol nunca cambia', 'las capacidades declaradas son siempre callables tras la resolución', 'este módulo no modifica el estado de otros módulos', 'este módulo no in
      [20]
        nombre: MODOS_ENTRADA
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['conversacion', 'afirmacion', 'teorema', 'auditoria', 'texto_libre', 'repositorio']
      [21]
        nombre: NOMBRE_MODULO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'contexto'
      [22]
        nombre: Path
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: clase
        estado: descubierto
        errores:
          []
      [23]
        nombre: REGLA_CAMPOS_OBLIGATORIOS
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['id', 'nombre', 'version', 'descripcion']
      [24]
        nombre: ROL_MODULO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'CX'
      [25]
        nombre: TIPOS_PETICION
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['por_que_valor', 'dame_O', 'dame_evidencia', 'dame_normas', 'dame_limites', 'dame_cadena_completa']
      [26]
        nombre: VERSION_CONTRATO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: '1.0'
      [27]
        nombre: VERSION_MODULO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: '2.3'
      [28]
        nombre: _CAP_MAP
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: {'resolver': <function resolver at 0x7fdcf221b2e0>, 'evaluar': <function resolver at 0x7fdcf221b2e0>, 'centinela': <function centinela at 0x7fdcf221b240>, 'barrer': <function barrer at 0x7fdcf221b380>
      [29]
        nombre: _Undefined
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: clase
        estado: descubierto
        errores:
          []
      [30]
        nombre: __all__
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['CONTENEDOR', 'ID_MODULO', 'NOMBRE_MODULO', 'ROL_MODULO', 'VERSION_MODULO', 'VERSION_CONTRATO', 'ESQUEMA_CONTRATO', 'ESTABILIDAD', 'UNDEFINED', 'es_undefined', 'ContextoError', 'ContratoInvalido', 'r
      [31]
        nombre: __annotations__
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: {'CONTENEDOR': 'Dict[str, Any]'}
      [32]
        nombre: __path__
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['/home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto']
      [33]
        nombre: _asegurar_invariante_pedir_anuncio
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _asegurar_invariante_pedir_anuncio at 0x7fdcf221aac0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [34]
        nombre: _cargar_reglas
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _cargar_reglas at 0x7fdcf221afc0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [35]
        nombre: _centinela_archivo
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _centinela_archivo at 0x7fdcf221af20>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [36]
        nombre: _cfg
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _cfg at 0x7fdcf221a840>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [37]
        nombre: _conflicto_ligaduras
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _conflicto_ligaduras at 0x7fdcf221ac00>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [38]
        nombre: _descubrir_inventario_total
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _descubrir_inventario_total at 0x7fdcf221b1a0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [39]
        nombre: _detectar_choques_reglas
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _detectar_choques_reglas at 0x7fdcf221b060>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [40]
        nombre: _id_anclado
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _id_anclado at 0x7fdcf221ad40>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [41]
        nombre: _normalizar_registro
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _normalizar_registro at 0x7fdcf221ab60>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [42]
        nombre: _normalizar_tipos_peticion
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _normalizar_tipos_peticion at 0x7fdcf221aa20>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [43]
        nombre: _permite_k
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _permite_k at 0x7fdcf221aca0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [44]
        nombre: _registro_vacio
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _registro_vacio at 0x7fdcf221a8e0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [45]
        nombre: _resolver_capacidades
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _resolver_capacidades at 0x7fdcf221ba60>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [46]
        nombre: _truthy_pedir
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _truthy_pedir at 0x7fdcf221a980>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [47]
        nombre: _validar_clasificacion
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _validar_clasificacion at 0x7fdcf221ae80>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [48]
        nombre: _validar_contrato
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _validar_contrato at 0x7fdcf221b100>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [49]
        nombre: _validar_regla_meta
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _validar_regla_meta at 0x7fdcf221ade0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [50]
        nombre: axiomas
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function axiomas at 0x7fdcf221b740>
        ejecutable_directamente: True
      [51]
        nombre: barrer
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function barrer at 0x7fdcf221b380>
        ejecutable_directamente: True
      [52]
        nombre: centinela
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function centinela at 0x7fdcf221b240>
        ejecutable_directamente: True
      [53]
        nombre: dataclass
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function dataclass at 0x7fdcf24ee480>
        ejecutable_directamente: True
      [54]
        nombre: defaultdict
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: clase
        estado: descubierto
        errores:
          []
      [55]
        nombre: deque
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: clase
        estado: descubierto
        errores:
          []
      [56]
        nombre: diagnostico
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function diagnostico at 0x7fdcf221b9c0>
        ejecutable_directamente: True
      [57]
        nombre: ejecutar
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function ejecutar at 0x7fdcf221b6a0>
        ejecutable_directamente: True
      [58]
        nombre: es_undefined
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function es_undefined at 0x7fdcf21d4040>
        ejecutable_directamente: False
      [59]
        nombre: evaluar_universal
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function evaluar_universal at 0x7fdcf221b880>
        ejecutable_directamente: True
      [60]
        nombre: field
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function field at 0x7fdcf24efd80>
        ejecutable_directamente: True
      [61]
        nombre: inventario
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function inventario at 0x7fdcf221b600>
        ejecutable_directamente: True
      [62]
        nombre: recibir_comentarios
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function recibir_comentarios at 0x7fdcf221b7e0>
        ejecutable_directamente: False
      [63]
        nombre: registrar_inventario
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function registrar_inventario at 0x7fdcf221b560>
        ejecutable_directamente: True
      [64]
        nombre: reporte
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function reporte at 0x7fdcf221b920>
        ejecutable_directamente: True
      [65]
        nombre: resolver
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function resolver at 0x7fdcf221b2e0>
        ejecutable_directamente: True
      [66]
        nombre: verificar
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function verificar at 0x7fdcf221b420>
        ejecutable_directamente: True
      [67]
        nombre: verificar_salida
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function verificar_salida at 0x7fdcf221b4c0>
        ejecutable_directamente: False
      [68]
        nombre: auto_auditoria
        tipo: regla
        origen: auto_auditoria.py
        modulo: contexto
        archivo: auto_auditoria.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [69]
        nombre: declaracion_O
        tipo: validador
        origen: declaracion_O.py
        modulo: contexto
        archivo: declaracion_O.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [70]
        nombre: entendimiento_fractal
        tipo: validador
        origen: entendimiento_fractal.py
        modulo: contexto
        archivo: entendimiento_fractal.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [71]
        nombre: entrada_natural
        tipo: validador
        origen: entrada_natural.py
        modulo: contexto
        archivo: entrada_natural.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [72]
        nombre: marco_desde_repositorio
        tipo: validador
        origen: marco_desde_repositorio.py
        modulo: contexto
        archivo: marco_desde_repositorio.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [73]
        nombre: nucleo_sm_CX
        tipo: validador
        origen: nucleo_sm_CX.py
        modulo: contexto
        archivo: nucleo_sm_CX.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [74]
        nombre: peticion_anuncio
        tipo: validador
        origen: peticion_anuncio.py
        modulo: contexto
        archivo: peticion_anuncio.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [75]
        nombre: secuencia_conversacion
        tipo: validador
        origen: secuencia_conversacion.py
        modulo: contexto
        archivo: secuencia_conversacion.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
    funciones:
      [0]
        nombre: _asegurar_invariante_pedir_anuncio
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _asegurar_invariante_pedir_anuncio at 0x7fdcf221aac0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [1]
        nombre: _cargar_reglas
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _cargar_reglas at 0x7fdcf221afc0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [2]
        nombre: _centinela_archivo
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _centinela_archivo at 0x7fdcf221af20>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [3]
        nombre: _cfg
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _cfg at 0x7fdcf221a840>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [4]
        nombre: _conflicto_ligaduras
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _conflicto_ligaduras at 0x7fdcf221ac00>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [5]
        nombre: _descubrir_inventario_total
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _descubrir_inventario_total at 0x7fdcf221b1a0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [6]
        nombre: _detectar_choques_reglas
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _detectar_choques_reglas at 0x7fdcf221b060>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [7]
        nombre: _id_anclado
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _id_anclado at 0x7fdcf221ad40>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [8]
        nombre: _normalizar_registro
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _normalizar_registro at 0x7fdcf221ab60>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [9]
        nombre: _normalizar_tipos_peticion
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _normalizar_tipos_peticion at 0x7fdcf221aa20>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [10]
        nombre: _permite_k
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _permite_k at 0x7fdcf221aca0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [11]
        nombre: _registro_vacio
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _registro_vacio at 0x7fdcf221a8e0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [12]
        nombre: _resolver_capacidades
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _resolver_capacidades at 0x7fdcf221ba60>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [13]
        nombre: _truthy_pedir
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _truthy_pedir at 0x7fdcf221a980>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [14]
        nombre: _validar_clasificacion
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _validar_clasificacion at 0x7fdcf221ae80>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [15]
        nombre: _validar_contrato
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _validar_contrato at 0x7fdcf221b100>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [16]
        nombre: _validar_regla_meta
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function _validar_regla_meta at 0x7fdcf221ade0>
        ejecutable_directamente: False
        participa_en_ejecucion: True
      [17]
        nombre: axiomas
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function axiomas at 0x7fdcf221b740>
        ejecutable_directamente: True
      [18]
        nombre: barrer
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function barrer at 0x7fdcf221b380>
        ejecutable_directamente: True
      [19]
        nombre: centinela
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function centinela at 0x7fdcf221b240>
        ejecutable_directamente: True
      [20]
        nombre: dataclass
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function dataclass at 0x7fdcf24ee480>
        ejecutable_directamente: True
      [21]
        nombre: diagnostico
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function diagnostico at 0x7fdcf221b9c0>
        ejecutable_directamente: True
      [22]
        nombre: ejecutar
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function ejecutar at 0x7fdcf221b6a0>
        ejecutable_directamente: True
      [23]
        nombre: es_undefined
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function es_undefined at 0x7fdcf21d4040>
        ejecutable_directamente: False
      [24]
        nombre: evaluar_universal
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function evaluar_universal at 0x7fdcf221b880>
        ejecutable_directamente: True
      [25]
        nombre: field
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function field at 0x7fdcf24efd80>
        ejecutable_directamente: True
      [26]
        nombre: inventario
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function inventario at 0x7fdcf221b600>
        ejecutable_directamente: True
      [27]
        nombre: recibir_comentarios
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function recibir_comentarios at 0x7fdcf221b7e0>
        ejecutable_directamente: False
      [28]
        nombre: registrar_inventario
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function registrar_inventario at 0x7fdcf221b560>
        ejecutable_directamente: True
      [29]
        nombre: reporte
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function reporte at 0x7fdcf221b920>
        ejecutable_directamente: True
      [30]
        nombre: resolver
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function resolver at 0x7fdcf221b2e0>
        ejecutable_directamente: True
      [31]
        nombre: verificar
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function verificar at 0x7fdcf221b420>
        ejecutable_directamente: True
      [32]
        nombre: verificar_salida
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function verificar_salida at 0x7fdcf221b4c0>
        ejecutable_directamente: False
    clases:
      [0]
        nombre: Any
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: clase
        estado: descubierto
        errores:
          []
      [1]
        nombre: Path
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: clase
        estado: descubierto
        errores:
          []
      [2]
        nombre: _Undefined
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: clase
        estado: descubierto
        errores:
          []
      [3]
        nombre: defaultdict
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: clase
        estado: descubierto
        errores:
          []
      [4]
        nombre: deque
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: clase
        estado: descubierto
        errores:
          []
    constantes:
      [0]
        nombre: API_ENGINE
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: '>=1.0'
      [1]
        nombre: ARCHIVOS_PY
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: [PosixPath('/home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/__init__.py'), PosixPath('/home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto/auto_auditoria.py'), PosixPath('
      [2]
        nombre: CLAVES_FUERA_DE_DOMINIO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['Tru_Ri', 'Tru_total', 'tru_ri', 'tru_total', 'C', 'L', 'K', 'alpha', 'beta', 'ALPHA', 'BETA']
      [3]
        nombre: CLAVES_PEDIR_ANUNCIO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['pedir_anuncio', 'pedir_cita', 'anuncio', 'citar', 'cadena_auditable', 'dame_por_que']
      [4]
        nombre: COMPATIBLE_DESDE
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: '1.0'
      [5]
        nombre: CONTENEDOR
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: {'esquema': 'VPSI-CONTRACT-1.0', 'version_contrato': '1.0', 'version_modulo': '2.3', 'estabilidad': 'ESTABLE', 'compatible_desde': '1.0', 'api_engine': '>=1.0', 'id': 'CX', 'nombre': 'contexto', 'rol'
      [6]
        nombre: ESQUEMA_CONTRATO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'VPSI-CONTRACT-1.0'
      [7]
        nombre: ESTABILIDAD
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'ESTABLE'
      [8]
        nombre: ESTADOS_O
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['estable', 'cambio', 'indefinido']
      [9]
        nombre: ESTADOS_VALIDOS
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ('NO_INICIADO', 'OPERATIVO', 'DEGRADADO', 'RECHAZADO')
      [10]
        nombre: ESTADO_DEGRADADO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'DEGRADADO'
      [11]
        nombre: ESTADO_NO_INICIADO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'NO_INICIADO'
      [12]
        nombre: ESTADO_OPERATIVO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'OPERATIVO'
      [13]
        nombre: ESTADO_RECHAZADO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'RECHAZADO'
      [14]
        nombre: EVENTOS
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['mismo_O', 'expansion', 'cambio', 'indefinido']
      [15]
        nombre: ID_MODULO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'CX'
      [16]
        nombre: INVARIANTES
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ('el id del módulo nunca cambia', 'el rol nunca cambia', 'las capacidades declaradas son siempre callables tras la resolución', 'este módulo no modifica el estado de otros módulos', 'este módulo no in
      [17]
        nombre: MODOS_ENTRADA
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['conversacion', 'afirmacion', 'teorema', 'auditoria', 'texto_libre', 'repositorio']
      [18]
        nombre: NOMBRE_MODULO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'contexto'
      [19]
        nombre: REGLA_CAMPOS_OBLIGATORIOS
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['id', 'nombre', 'version', 'descripcion']
      [20]
        nombre: ROL_MODULO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: 'CX'
      [21]
        nombre: TIPOS_PETICION
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['por_que_valor', 'dame_O', 'dame_evidencia', 'dame_normas', 'dame_limites', 'dame_cadena_completa']
      [22]
        nombre: VERSION_CONTRATO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: '1.0'
      [23]
        nombre: VERSION_MODULO
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: '2.3'
      [24]
        nombre: _CAP_MAP
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: {'resolver': <function resolver at 0x7fdcf221b2e0>, 'evaluar': <function resolver at 0x7fdcf221b2e0>, 'centinela': <function centinela at 0x7fdcf221b240>, 'barrer': <function barrer at 0x7fdcf221b380>
      [25]
        nombre: __all__
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['CONTENEDOR', 'ID_MODULO', 'NOMBRE_MODULO', 'ROL_MODULO', 'VERSION_MODULO', 'VERSION_CONTRATO', 'ESQUEMA_CONTRATO', 'ESTABILIDAD', 'UNDEFINED', 'es_undefined', 'ContextoError', 'ContratoInvalido', 'r
      [26]
        nombre: __annotations__
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: {'CONTENEDOR': 'Dict[str, Any]'}
      [27]
        nombre: __path__
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        requiere_entrada: False
        tipo: constante
        estado: descubierto
        errores:
          []
        representacion: ['/home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/contexto']
    excepciones:
      [0]
        nombre: ContextoError
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: excepcion
        estado: descubierto
        errores:
          []
      [1]
        nombre: ContratoInvalido
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: False
        requiere_entrada: False
        tipo: excepcion
        estado: descubierto
        errores:
          []
    clasificadores:
      []
    validadores:
      [0]
        nombre: declaracion_O
        tipo: validador
        origen: declaracion_O.py
        modulo: contexto
        archivo: declaracion_O.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [1]
        nombre: entendimiento_fractal
        tipo: validador
        origen: entendimiento_fractal.py
        modulo: contexto
        archivo: entendimiento_fractal.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [2]
        nombre: entrada_natural
        tipo: validador
        origen: entrada_natural.py
        modulo: contexto
        archivo: entrada_natural.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [3]
        nombre: marco_desde_repositorio
        tipo: validador
        origen: marco_desde_repositorio.py
        modulo: contexto
        archivo: marco_desde_repositorio.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [4]
        nombre: nucleo_sm_CX
        tipo: validador
        origen: nucleo_sm_CX.py
        modulo: contexto
        archivo: nucleo_sm_CX.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [5]
        nombre: peticion_anuncio
        tipo: validador
        origen: peticion_anuncio.py
        modulo: contexto
        archivo: peticion_anuncio.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
      [6]
        nombre: secuencia_conversacion
        tipo: validador
        origen: secuencia_conversacion.py
        modulo: contexto
        archivo: secuencia_conversacion.py
        declarado: False
        descubierto: True
        callable: False
        ejecutable: False
        estado: descubierto
        errores:
          []
    unidades_ejecutables:
      [0]
        nombre: axiomas
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function axiomas at 0x7fdcf221b740>
        ejecutable_directamente: True
      [1]
        nombre: barrer
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function barrer at 0x7fdcf221b380>
        ejecutable_directamente: True
      [2]
        nombre: centinela
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function centinela at 0x7fdcf221b240>
        ejecutable_directamente: True
      [3]
        nombre: dataclass
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function dataclass at 0x7fdcf24ee480>
        ejecutable_directamente: True
      [4]
        nombre: diagnostico
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function diagnostico at 0x7fdcf221b9c0>
        ejecutable_directamente: True
      [5]
        nombre: ejecutar
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function ejecutar at 0x7fdcf221b6a0>
        ejecutable_directamente: True
      [6]
        nombre: es_undefined
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function es_undefined at 0x7fdcf21d4040>
        ejecutable_directamente: False
      [7]
        nombre: evaluar_universal
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function evaluar_universal at 0x7fdcf221b880>
        ejecutable_directamente: True
      [8]
        nombre: field
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function field at 0x7fdcf24efd80>
        ejecutable_directamente: True
      [9]
        nombre: inventario
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function inventario at 0x7fdcf221b600>
        ejecutable_directamente: True
      [10]
        nombre: recibir_comentarios
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: False
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function recibir_comentarios at 0x7fdcf221b7e0>
        ejecutable_directamente: False
      [11]
        nombre: registrar_inventario
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function registrar_inventario at 0x7fdcf221b560>
        ejecutable_directamente: True
      [12]
        nombre: reporte
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function reporte at 0x7fdcf221b920>
        ejecutable_directamente: True
      [13]
        nombre: resolver
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function resolver at 0x7fdcf221b2e0>
        ejecutable_directamente: True
      [14]
        nombre: verificar
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: False
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function verificar at 0x7fdcf221b420>
        ejecutable_directamente: True
      [15]
        nombre: verificar_salida
        origen: vpsi_dinamico_contexto
        modulo: contexto
        archivo: __init__.py
        declarado: True
        descubierto: True
        callable: True
        ejecutable: True
        requiere_entrada: True
        tipo: funcion
        estado: descubierto
        errores:
          []
        referencia: <function verificar_salida at 0x7fdcf221b4c0>
        ejecutable_directamente: False
    total_componentes: 76
    total_ejecutables: 16

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
    • CE
    • AX
    • FO
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    evaluar_universal: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
  capacidades:
    • axiomas
    • barrer
    • diagnostico
    • ejecutar_total
    • evaluar
    • evaluar_universal
    • inspeccionar
    • inventario
    • listar_mecanicas
    • registrar_inventario
    • reporte
    • verificar
    • verificar_salida
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia mecánica.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con coherente, choques, errores, mecanica, archivos
      acceso_archivos:
        • *
    barrer:
      descripcion: Lee todas las MECANICA de la carpeta, calcula orden, detecta contradicciones o ciclos y notifica a DiagnosticoGlobal.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con estado, coherente, choques, errores, mecanica, archivos
      acceso_archivos:
        • *
    evaluar:
      descripcion: Alias de barrer. Evalúa coherencia del núcleo MC.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con estado, coherente, choques, errores, mecanica
      acceso_archivos:
        • *
    axiomas:
      descripcion: Declaraciones internas de correlación (CORR_SEQ_01, CORR_SEQ_02).
      entrada: ninguna
      validar_esquema:
        • *
      salida: list[dict] de declaraciones
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario objetivo de mecánicas declaradas en la carpeta.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con total_mecanicas, archivos, declaran
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Comprueba si una salida de barrer es coherente.
      entrada: salida: dict
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte interno de estado del módulo MC.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con estado, coherente, choques, errores, capacidades
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico: qué falta, qué está mal en MC.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    listar_mecanicas:
      descripcion: Lista todas las MECANICA descubiertas en la carpeta.
      entrada: ninguna
      validar_esquema:
        • *
      salida: dict archivo → meta MECANICA
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre MC. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de MC. Expone constantes, capacidades, mecanicas y estado sin alterar el contrato ni calcular.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de MC como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
      • __init__.py: error estructural: name 'ast' is not defined
      • calculo_CICLO.py: error estructural: name 'ast' is not defined
      • calculo_variables_AX.py: error estructural: name 'ast' is not defined
      • causalidad_universal.py: error estructural: name 'ast' is not defined
      • citacion_MC.py: error estructural: name 'ast' is not defined
      • contexto_MC.py: error estructural: name 'ast' is not defined
      • contexto_fractal_MC.py: error estructural: name 'ast' is not defined
      • grafo_I_MC.py: error estructural: name 'ast' is not defined
      • ley_coherencia_MC.py: error estructural: name 'ast' is not defined
      • mecanica_preguntas.py: error estructural: name 'ast' is not defined
      • mechanic_of_the_mechanics.py: error estructural: name 'ast' is not defined
      • principio_asociacion_MC.py: error estructural: name 'ast' is not defined
      • realidad_MC.py: error estructural: name 'ast' is not defined
      • sm_nucleo_MC.py: error estructural: name 'ast' is not defined
    mecanica:
      []
    archivos:
      • calculo_CICLO.py
      • calculo_variables_AX.py
      • causalidad_universal.py
      • citacion_MC.py
      • contexto_MC.py
      • contexto_fractal_MC.py
      • grafo_I_MC.py
      • ley_coherencia_MC.py
      • mecanica_preguntas.py
      • mechanic_of_the_mechanics.py
      • principio_asociacion_MC.py
      • realidad_MC.py
      • sm_nucleo_MC.py
    total_mecanicas: 13
    capacidades:
      • axiomas
      • barrer
      • diagnostico
      • ejecutar_total
      • evaluar
      • evaluar_universal
      • inspeccionar
      • inventario
      • listar_mecanicas
      • registrar_inventario
      • reporte
      • verificar
      • verificar_salida
    requiere:
      • CE
      • AX
      • FO
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
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
          • __init__.py: error estructural: name 'ast' is not defined
          • calculo_CICLO.py: error estructural: name 'ast' is not defined
          • calculo_variables_AX.py: error estructural: name 'ast' is not defined
          • causalidad_universal.py: error estructural: name 'ast' is not defined
          • citacion_MC.py: error estructural: name 'ast' is not defined
          • contexto_MC.py: error estructural: name 'ast' is not defined
          • contexto_fractal_MC.py: error estructural: name 'ast' is not defined
          • grafo_I_MC.py: error estructural: name 'ast' is not defined
          • ley_coherencia_MC.py: error estructural: name 'ast' is not defined
          • mecanica_preguntas.py: error estructural: name 'ast' is not defined
          • mechanic_of_the_mechanics.py: error estructural: name 'ast' is not defined
          • principio_asociacion_MC.py: error estructural: name 'ast' is not defined
          • realidad_MC.py: error estructural: name 'ast' is not defined
          • sm_nucleo_MC.py: error estructural: name 'ast' is not defined
    advertencias:
      []
    recomendaciones:
      • Revisar las declaraciones MECANICA que presentan errores estructurales o de carga
    coherente: False
    choques_n: 0
    errores_n: 14
    total_mecanicas: 13
  inventario:
    id: MC
    nombre: correlacion_mecanica
    rol: MC
    version: 1.3
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    total_mecanicas: 13
    archivos:
      • calculo_CICLO.py
      • calculo_variables_AX.py
      • causalidad_universal.py
      • citacion_MC.py
      • contexto_MC.py
      • contexto_fractal_MC.py
      • grafo_I_MC.py
      • ley_coherencia_MC.py
      • mecanica_preguntas.py
      • mechanic_of_the_mechanics.py
      • principio_asociacion_MC.py
      • realidad_MC.py
      • sm_nucleo_MC.py
    declaran:
      calculo_CICLO.py:
        nombre: Cálculo de Variables de Verdad (C, L, K) bajo anclas AM
        version: 2.0
        n_nodos: 8
      calculo_variables_AX.py:
        nombre: Cálculo de Variables de Verdad (C, L, K) bajo anclas AM
        version: 2.0
        n_nodos: 8
      causalidad_universal.py:
        nombre: causalidad_universal
        version: NO ENTREGADO POR ENGINE
        n_nodos: 21
      citacion_MC.py:
        nombre: citacion_mecanica
        version: 0.1
        n_nodos: 14
      contexto_MC.py:
        nombre: contexto_mecanico
        version: 0.2
        n_nodos: 11
      contexto_fractal_MC.py:
        nombre: contexto_fractal_mecanico
        version: 1.0
        n_nodos: 14
      grafo_I_MC.py:
        nombre: grafo_mc
        version: 1.3
        n_nodos: 24
      ley_coherencia_MC.py:
        nombre: ley_coherencia_MC
        version: 2.1
        n_nodos: 14
      mecanica_preguntas.py:
        nombre: mecanica_preguntas
        version: NO ENTREGADO POR ENGINE
        n_nodos: 19
      mechanic_of_the_mechanics.py:
        nombre: mechanic_of_the_mechanics
        version: 1.0
        n_nodos: 18
      principio_asociacion_MC.py:
        nombre: principio_asociacion_MC
        version: 1.3
        n_nodos: 44
      realidad_MC.py:
        nombre: realidad_MC
        version: 1.0
        n_nodos: 23
      sm_nucleo_MC.py:
        nombre: sm_nucleo_mecanica
        version: 1.0
        n_nodos: 18
    coherente: False
    choques:
      []
    errores:
      • __init__.py: error estructural: name 'ast' is not defined
      • calculo_CICLO.py: error estructural: name 'ast' is not defined
      • calculo_variables_AX.py: error estructural: name 'ast' is not defined
      • causalidad_universal.py: error estructural: name 'ast' is not defined
      • citacion_MC.py: error estructural: name 'ast' is not defined
      • contexto_MC.py: error estructural: name 'ast' is not defined
      • contexto_fractal_MC.py: error estructural: name 'ast' is not defined
      • grafo_I_MC.py: error estructural: name 'ast' is not defined
      • ley_coherencia_MC.py: error estructural: name 'ast' is not defined
      • mecanica_preguntas.py: error estructural: name 'ast' is not defined
      • mechanic_of_the_mechanics.py: error estructural: name 'ast' is not defined
      • principio_asociacion_MC.py: error estructural: name 'ast' is not defined
      • realidad_MC.py: error estructural: name 'ast' is not defined
      • sm_nucleo_MC.py: error estructural: name 'ast' is not defined
    mecanica:
      []
    capacidades:
      • axiomas
      • barrer
      • diagnostico
      • ejecutar_total
      • evaluar
      • evaluar_universal
      • inspeccionar
      • inventario
      • listar_mecanicas
      • registrar_inventario
      • reporte
      • verificar
      • verificar_salida
    requiere:
      • CE
      • AX
      • FO
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no inventa mecánicas no declaradas en archivos
      • este módulo siempre puede reportar su propio estado
    declaraciones_n: 2

══════════════════════════════════════════════════════════════════════
  MÓDULO DGCO/diagnosticoD
══════════════════════════════════════════════════════════════════════
  id: DGCO
  nombre: diagnosticoD
  rol: DGCO
  version: 1.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Diagnóstico global por conteo de capacidades de todos los módulos. Solo lectura. No calcula Tru. No orquesta. Sin pesos.
  funcion: Contar capacidades presentes y faltantes por módulo, sumar el sistema completo y exponer censo/diagnóstico global.
  no_hace:
    • No calcula Tru
    • No usa pesos
    • No orquesta el ciclo
    • No modifica módulos auditados
    • No altera evidencia recibida
    • No importa core.diagnosticoD
  autoridad:
    • Auditar capacidades de cada módulo
    • Consolidar censo global por conteo
    • Recibir reportes de módulos
    • Exponer inventario y diagnóstico propios
  conocimiento_exportable:
    • censo
    • verificar
    • barrer
    • presentar
    • reportar
    • inventario
    • reporte
    • diagnostico
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  consultas_soportadas:
    • censo
    • verificar
    • barrer
    • presentar
    • reportar
    • inventario
    • reporte
    • diagnostico
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  requiere:
    • *
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
  capacidades:
    • censo
    • verificar
    • barrer
    • presentar
    • reportar
    • inventario
    • reporte
    • diagnostico
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    censo:
      descripcion: Censo global por conteo de capacidades.
      entrada: engine opcional
      validar_esquema:
        • *
      salida: dict con totales, presentes, faltantes, modulos
      acceso_archivos:
        • *
    verificar:
      descripcion: Centinela de coherencia global por conteo.
      entrada: engine opcional
      validar_esquema:
        • *
      salida: dict con coherente, totales, faltantes
      acceso_archivos:
        • *
    barrer:
      descripcion: Alias de verificar.
      entrada: engine opcional
      validar_esquema:
        • *
      salida: dict con coherente, totales, faltantes
      acceso_archivos:
        • *
    presentar:
      descripcion: Presenta el censo global formateado.
      entrada: informe opcional
      validar_esquema:
        • *
      salida: str
      acceso_archivos:
        • *
    reportar:
      descripcion: Recibe reporte de un módulo.
      entrada: modulo, errores
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario contractual de DGCO.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, capacidades, regla
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte de estado de DGCO.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, coherente
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico propio de DGCO.
      entrada: *
      validar_esquema:
        • *
      salida: dict con problemas, advertencias
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre DGCO.
      entrada: peticion opcional
      validar_esquema:
        • *
      salida: dict con resultados
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Inspección estructural de DGCO.
      entrada: peticion opcional
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Instantánea determinista del inventario de DGCO.
      entrada: peticion opcional
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • DGCO no calcula Tru
    • DGCO no orquesta el ciclo
    • DGCO no altera evidencia recibida
    • DGCO diagnostica solo por conteo de capacidades
    • DGCO no usa pesos
    • las capacidades declaradas son callables tras la resolución
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
  reporte:
    id: DGCO
    modulo: diagnosticoD
    rol: DGCO
    version: 1.0
    estado: OPERATIVO
    coherente: True
    capacidades:
      • censo
      • verificar
      • barrer
      • presentar
      • reportar
      • inventario
      • reporte
      • diagnostico
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    nota: DGCO observa por conteo; no invalida arranque por sí solo.
  diagnostico:
    id: DGCO
    modulo: diagnosticoD
    estado: OPERATIVO
    coherente: True
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    nota: Diagnóstico propio de DGCO. La regla global vive en censo().
  inventario:
    id: DGCO
    nombre: diagnosticoD
    rol: DGCO
    version: 1.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    capacidades:
      • censo
      • verificar
      • barrer
      • presentar
      • reportar
      • inventario
      • reporte
      • diagnostico
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    regla: por módulo: faltantes==0 y total>0 → OPERATIVO; global = suma de conteos
    requiere:
      • *
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • DGCO no calcula Tru
      • DGCO no orquesta el ciclo
      • DGCO no altera evidencia recibida
      • DGCO diagnostica solo por conteo de capacidades
      • DGCO no usa pesos
      • las capacidades declaradas son callables tras la resolución
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
    nota: DGCO autónomo. Sin core. Sin pesos.

══════════════════════════════════════════════════════════════════════
  MÓDULO DI/diccionario
══════════════════════════════════════════════════════════════════════
  id: DI
  nombre: diccionario
  rol: DI
  version: 1.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Biblioteca de definiciones. Rol DI. Materia prima léxica: palabra → definición → significado. Herramienta para contrastar y correlacionar a nivel de significado. Auto-carga todos los archivos debajo del módulo. Engine puede solicitar y distribuir definiciones según contexto. No calcula Tru. No clasifica O. No trae dominios externos.
  funcion: Biblioteca de definiciones para contrastar y correlacionar a nivel léxico-significado. Materia prima: palabra → definición → significado. Auto-carga todo lo que está debajo del módulo.
  no_hace:
    • No calcula C, L, K, Tru_Ri ni Tru_total
    • No clasifica O_context (eso es CX)
    • No trae material externo de dominios (eso es RE)
    • No orquesta el ciclo (eso es Engine)
    • No sustituye AX, MC, CA, FO, CIT
  autoridad:
    • Exponer definiciones y significados
    • Auto-cargar todos los archivos que declaren DICCIONARIO
    • Entregar materia prima léxica a Engine y otros módulos
    • Reportar estado, inventario y diagnóstico propios
  conocimiento_exportable:
    • inventario
    • reporte
    • diagnostico
    • listar
    • cargar
    • cargar_todos
    • definir
    • significado
    • palabras
    • inyectar_en_peticion
    • verificar
    • barrer
    • resolver
    • axiomas
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  consultas_soportadas:
    • listar
    • cargar
    • cargar_todos
    • definir
    • significado
    • palabras
    • inyectar_en_peticion
    • inventario
    • reporte
    • diagnostico
    • verificar
    • barrer
    • resolver
    • axiomas
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
  capacidades:
    • verificar
    • barrer
    • verificar_salida
    • inventario
    • reporte
    • diagnostico
    • axiomas
    • resolver
    • listar
    • cargar
    • cargar_todos
    • definir
    • significado
    • palabras
    • inyectar_en_peticion
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia del diccionario.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, errores, diccionarios, total
      acceso_archivos:
        • *
    barrer:
      descripcion: Centinela de DI: valida forma de las fuentes, reporta errores de carga. No calcula Tru.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, errores, diccionarios, total, por_idioma
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario de diccionarios descubiertos.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, version, total, diccionarios, por_idioma
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte interno de estado del módulo DI.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, estado, coherente, diccionarios, capacidades
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico del módulo DI.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    axiomas:
      descripcion: Declaraciones axiomáticas del módulo DI.
      entrada: *
      validar_esquema:
        • *
      salida: list[dict] de declaraciones
      acceso_archivos:
        • *
    resolver:
      descripcion: Entrega definiciones según palabra, idioma o fuente.
      entrada: *
      validar_esquema:
        • *
      salida: dict con definiciones o materia prima
      acceso_archivos:
        • *
    listar:
      descripcion: Nombres de todos los diccionarios descubiertos.
      entrada: *
      validar_esquema:
        • *
      salida: list[str]
      acceso_archivos:
        • *
    cargar:
      descripcion: Carga un diccionario por nombre.
      entrada: *
      validar_esquema:
        • *
      salida: dict con el DICCIONARIO
      acceso_archivos:
        • *
    cargar_todos:
      descripcion: Carga todos los diccionarios descubiertos.
      entrada: *
      validar_esquema:
        • *
      salida: dict nombre → datos
      acceso_archivos:
        • *
    definir:
      descripcion: Busca definición de una palabra en fuentes.
      entrada: *
      validar_esquema:
        • *
      salida: dict con definicion, significado, fuente o None
      acceso_archivos:
        • *
    significado:
      descripcion: Atajo para obtener significado/definición de una palabra.
      entrada: *
      validar_esquema:
        • *
      salida: str o None
      acceso_archivos:
        • *
    palabras:
      descripcion: Conjunto de lemas de las fuentes indicadas.
      entrada: *
      validar_esquema:
        • *
      salida: set[str]
      acceso_archivos:
        • *
    inyectar_en_peticion:
      descripcion: Entrega lemas a una petición para el ciclo.
      entrada: *
      validar_esquema:
        • *
      salida: peticion con lemas inyectados
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Comprueba forma mínima de una salida de DI.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre DI. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de DI. Expone constantes, capacidades, diccionarios y estado sin alterar el contrato ni calcular.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de DI como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • DI es una herramienta de definiciones, no calcula Tru
    • DI no clasifica O_context (eso es CX)
    • DI auto-carga todo lo que está debajo del módulo
    • las capacidades declaradas son siempre callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
    • este módulo siempre puede reportar su propio estado
  reporte:
    id: DI
    modulo: diccionario
    rol: DI
    version: 1.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    diccionarios: 2
    errores: 0
    capacidades:
      • axiomas
      • barrer
      • cargar
      • cargar_todos
      • definir
      • diagnostico
      • ejecutar_total
      • evaluar_universal
      • inspeccionar
      • inventario
      • inyectar_en_peticion
      • listar
      • palabras
      • registrar_inventario
      • reporte
      • resolver
      • significado
      • verificar
      • verificar_salida
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
  diagnostico:
    id: DI
    modulo: diccionario
    estado: OPERATIVO
    coherente: True
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    diccionarios: 2
    errores_n: 0
  inventario:
    id: DI
    nombre: diccionario
    rol: DI
    version: 1.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    total: 2
    diccionarios:
      [0]
        nombre: en
        idioma: en
        tipo: registro_wordnet
        size: 0
        version: 2.0
        archivo: en.py
      [1]
        nombre: es
        idioma: es
        tipo: registro_wordnet
        size: 0
        version: 2.0
        archivo: es.py
    por_idioma:
      en:
        • en
      es:
        • es
    coherente: True
    capacidades:
      • axiomas
      • barrer
      • cargar
      • cargar_todos
      • definir
      • diagnostico
      • ejecutar_total
      • evaluar_universal
      • inspeccionar
      • inventario
      • inyectar_en_peticion
      • listar
      • palabras
      • registrar_inventario
      • reporte
      • resolver
      • significado
      • verificar
      • verificar_salida
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    autoridad:
      • Exponer definiciones y significados
      • Auto-cargar todos los archivos que declaren DICCIONARIO
      • Entregar materia prima léxica a Engine y otros módulos
      • Reportar estado, inventario y diagnóstico propios
    conocimiento_exportable:
      • inventario
      • reporte
      • diagnostico
      • listar
      • cargar
      • cargar_todos
      • definir
      • significado
      • palabras
      • inyectar_en_peticion
      • verificar
      • barrer
      • resolver
      • axiomas
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
    consultas_soportadas:
      • listar
      • cargar
      • cargar_todos
      • definir
      • significado
      • palabras
      • inyectar_en_peticion
      • inventario
      • reporte
      • diagnostico
      • verificar
      • barrer
      • resolver
      • axiomas
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • DI es una herramienta de definiciones, no calcula Tru
      • DI no clasifica O_context (eso es CX)
      • DI auto-carga todo lo que está debajo del módulo
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
      • este módulo siempre puede reportar su propio estado

══════════════════════════════════════════════════════════════════════
  MÓDULO FO/formulas
══════════════════════════════════════════════════════════════════════
  id: FO
  nombre: formulas
  rol: FO
  version: 2.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Contenedor de fórmulas. Expone y ejecuta tru_ri y tru_total y cualquier fórmula descubierta en los archivos del módulo. ALPHA y BETA se resuelven exclusivamente desde modules.constante.
  funcion: Ser la fuente oficial de las fórmulas de verdad: descubrir archivos, registrar fórmulas, evaluar tru_ri(C,L,K) y tru_total(C,L,K), validar coherencia.
  no_hace:
    • No calcula C, L, K (los recibe como entrada)
    • No clasifica entrada de usuario
    • No orquesta el sistema (eso es Engine)
    • No modifica otros módulos
  autoridad:
    • Ejecutar cualquier fórmula registrada o descubierta
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
    • CE
    • AX
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
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
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia de fórmulas.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, faltas, reglas, formulas
      acceso_archivos:
        • *
    barrer:
      descripcion: Barrido universal de todas las fórmulas del módulo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, coherente, faltas, formulas, verdad
      acceso_archivos:
        • *
    evaluar:
      descripcion: Alias de barrer.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, coherente, faltas, formulas
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Comprueba forma mínima de una salida de barrer.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario completo de fórmulas descubiertas y registradas.
      entrada: *
      validar_esquema:
        • *
      salida: dict con formulas, verdad, reglas, declaraciones
      acceso_archivos:
        • *
    axiomas:
      descripcion: Declaraciones FO-1 a FO-4.
      entrada: *
      validar_esquema:
        • *
      salida: list[dict]
      acceso_archivos:
        • *
    tru_ri:
      descripcion: Calcula Tru_Ri = C * L * K sin límites artificiales.
      entrada: C, L, K (Fraction)
      validar_esquema:
        • *
      salida: Fraction
      acceso_archivos:
        • *
    tru_total:
      descripcion: Calcula Tru_total = (Tru_Ri * ALPHA) + BETA.
      entrada: C, L, K (Fraction)
      validar_esquema:
        • *
      salida: Fraction
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte de estado del módulo FO.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, coherente, formulas, faltas
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico de faltas y recomendaciones.
      entrada: *
      validar_esquema:
        • *
      salida: dict con problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    listar_formulas:
      descripcion: Lista todas las fórmulas existentes.
      entrada: *
      validar_esquema:
        • *
      salida: dict con descubiertas, registradas, todas, verdad
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de Engine. Ejecuta todas las capacidades reales.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Inspección estructural sin calcular ni alterar.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con estructura, capacidades y estado
      acceso_archivos:
        • *
    registrar_inventario:
      descripcion: Instantánea determinista del inventario.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con inventario registrado
      acceso_archivos:
        • *
    evaluar_universal:
      descripcion: Evalúa capacidades reales cuya firma se satisfaga con los hechos.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
    • ALPHA y BETA provienen exclusivamente de modules.constante
  reporte:
    id: FO
    modulo: formulas
    rol: FO
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    faltas:
      []
    formulas:
      • escala
      • tru_ri
      • tru_total
      • verdad
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    autoridad:
      • Ejecutar cualquier fórmula registrada o descubierta
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
    formulas_n: 4
  inventario:
    id: FO
    nombre: formulas
    rol: FO
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    formulas:
      • escala
      • tru_ri
      • tru_total
      • verdad
    formulas_descubiertas:
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
    total_formulas: 4
    verdad:
      tru_ri: True
      tru_total: True
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
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • tru_ri y tru_total no imponen límites artificiales sobre C, L, K
      • ALPHA y BETA provienen exclusivamente de modules.constante

══════════════════════════════════════════════════════════════════════
  MÓDULO UI/interfaz
══════════════════════════════════════════════════════════════════════
  id: UI
  nombre: interfaz
  rol: UI
  version: 1.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Diseño de presentación del sistema. Compone descripciones de interfaz bajo un pedido explícito y lo observable (CACHE). Cero actuación sobre evaluación.
  funcion: Diseña descripciones de interfaz correlacionadas al mecanismo; vela sus paquetes; no calcula Tru.
  no_hace:
    • No calcula Tru_total ni Tru_Ri
    • No escribe C/L/K
    • No orquesta el ciclo Engine
    • No aprueba su propia salida de diseño
    • No inventa controles sin componente real
  autoridad:
    • Componer descripciones de interfaz
    • Inventariar paquetes de diseño
    • Observar pedido + evidencia CACHE
    • Verificar coherencia interna de paquetes y contrato
    • Reportar estado propio
  conocimiento_exportable:
    • componer
    • observar
    • inventario
    • inventario_paquetes
    • barrer
    • verificar
    • axiomas
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  consultas_soportadas:
    • componer
    • observar
    • inventario
    • inventario_paquetes
    • barrer
    • verificar
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: False
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    metricas: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    diagnostico: True
    reporte: True
    crear: False
    actualizar: False
    validar_esquema: True
    validar: True
    procesar: False
    analizar: False
    generar: True
    exportar: True
    importar: False
    respaldar: False
    recuperar: False
    sincronizar: False
    monitorear: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
  capacidades:
    • verificar
    • barrer
    • componer
    • observar
    • axiomas
    • inventario
    • inventario_paquetes
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia interna del módulo.
      entrada: ninguna
      salida: dict con id, nombre, rol, coherente, choques, errores, advertencias, paquetes
      validar_esquema:
        • *
      acceso_archivos:
        • *
    barrer:
      descripcion: Centinela de carpeta + verificación estructural del CONTENEDOR.
      entrada: ninguna
      salida: dict con id, nombre, rol, coherente, choques, errores, advertencias, paquetes_n
      validar_esquema:
        • *
      acceso_archivos:
        • *
    componer:
      descripcion: Genera descripción de interfaz (esquema). No inventa controles.
      entrada: peticion: dict con O_uso, superficie, zonas, layout
      salida: dict con id, nombre, rol, estado (PROPUESTO|PARCIAL|RETENIDO), esquema, observacion, auditable_por_centinela
      validar_esquema:
        • *
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario estructural del módulo UI.
      entrada: peticion opcional
      salida: dict con id, nombre, rol, version, superficies, zonas, paquetes, capacidades
      validar_esquema:
        • *
      acceso_archivos:
        • *
    inventario_paquetes:
      descripcion: Lista los paquetes descubiertos bajo paquetes/.
      entrada: ninguna
      salida: dict con id, nombre, rol, dir, n, paquetes
      validar_esquema:
        • *
      acceso_archivos:
        • *
    observar:
      descripcion: Reúne pedido + evidencia CACHE (solo lectura).
      entrada: pedido y cache_snapshot opcionales
      salida: dict con id, nombre, rol, pedido, evidencia_cache
      validar_esquema:
        • *
      acceso_archivos:
        • *
    axiomas:
      descripcion: Declaraciones operativas del módulo UI.
      entrada: ninguna
      salida: list[dict] de axiomas operativos
      validar_esquema:
        • *
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre UI. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      salida: dict con resultados de todas las unidades ejecutadas
      validar_esquema:
        • *
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de UI. Expone constantes, capacidades, paquetes y estado sin alterar el contrato ni calcular.
      entrada: peticion opcional (dict)
      salida: dict con estructura, capacidades y estado del modulo
      validar_esquema:
        • acceso_archivos
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de UI como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      salida: dict con inventario registrado
      validar_esquema:
        • acceso_archivos
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
    • no calcula ni modifica C, L, K ni Tru
    • no orquesta el ciclo Engine
    • toda salida de componer es auditable por Centinela (declaración)
    • presentar no forma parte de v1.0
    • los estados de operación de componer (PROPUESTO|PARCIAL|RETENIDO) son distintos de los estados del módulo
  reporte: NO ENTREGADO POR ENGINE
  diagnostico: NO ENTREGADO POR ENGINE
  inventario:
    id: UI
    nombre: interfaz
    rol: UI
    version: 1.0
    superficies:
      • web
      • desktop
      • mobile
      • cli
      • embebido
    zonas_canonicas:
      • contexto
      • estado_marco
      • reporte_simple
      • reporte_detalle
      • sistema
      • centinela
      • correlacion
    paquetes:
      id: UI
      nombre: interfaz
      rol: UI
      dir: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/modules/interfaz/paquetes
      n: 0
      paquetes:
    capacidades:
      • verificar
      • barrer
      • componer
      • observar
      • axiomas
      • inventario
      • inventario_paquetes
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    estados_operacion:
      • PROPUESTO
      • PARCIAL
      • RETENIDO
    nota: presentar no forma parte de v1.0

══════════════════════════════════════════════════════════════════════
  MÓDULO RE/realidad
══════════════════════════════════════════════════════════════════════
  id: RE
  nombre: realidad
  rol: RE
  version: 2.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Contenedor de realidad (RE). Ancla de contraste con representaciones de la realidad y dominios de conocimiento. Canal de acceso + dominios que declaran oficio y O de evaluación. Simbiosis: Engine aplica la fórmula bajo ese O; el material solo sube si el dominio aprueba; este módulo vela no-contradicción entre funciones del directorio. No calcula Tru.
  funcion: Descubrir y validar dominios/funciones del módulo; sostener el contrato de simbiosis dominio↔Engine; registrar aprobación o rechazo de material; reportar estado estructural propio.
  no_hace:
    • No calcula C, L, K, Tru_Ri ni Tru_total
    • No elige qué es verdad ni privilegia instituciones
    • No aprueba material en nombre de un dominio ajeno
    • No orquesta el ciclo completo del sistema
    • No deposita reportes en Diagnóstico
    • No sustituye el visto bueno de cada dominio
  autoridad:
    • Descubrir FUNCION en archivos y subcarpetas de dominio
    • Velar no-contradicción y unicidad de nombres de función
    • Registrar cierre contractual de material (aprobado/rechazado)
    • Exponer estado del canal de acceso
    • Reportar inventario, reporte y diagnóstico propios
  conocimiento_exportable:
    • inventario
    • reporte
    • diagnostico
    • funciones
    • dominios_simbiosis
    • estados_material
    • contrato_simbiosis
    • acceso
  consultas_soportadas:
    • verificar
    • barrer
    • inventario
    • reporte
    • diagnostico
    • registrar_resultado_dominio
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
  capacidades:
    • verificar
    • barrer
    • verificar_salida
    • inventario
    • reporte
    • diagnostico
    • registrar_resultado_dominio
    • ejecutar_total
    • inspeccionar
    • evaluar_universal
    • registrar_inventario
  capacidades_meta:
    verificar:
      descripcion: Garantiza la coherencia interna de RE (alias de barrer).
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, choques, errores, funciones
      acceso_archivos:
        • *
    barrer:
      descripcion: Centinela de no-contradicción entre dominios/funciones y registro de simbiosis dominio↔Engine.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, choques, errores, funciones, dominios_simbiosis, estados_material, notas
      acceso_archivos:
        • *
    inventario:
      descripcion: Enumeración de funciones, simbiosis y canal.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, version, funciones, coherente, acceso, contrato_simbiosis
      acceso_archivos:
        • *
    reporte:
      descripcion: Estado actual del módulo RE.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, version, capacidades, coherente
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Problemas, advertencias y recomendaciones de RE.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    registrar_resultado_dominio:
      descripcion: Cierra el tramo de simbiosis para un material: registra aprobación o rechazo del dominio tras resultado de Engine. No recalcula Tru.
      entrada: *
      validar_esquema:
        • *
      salida: dict con ok, estado, nota
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Forma mínima de una salida de RE.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre RE. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de RE. Expone constantes, capacidades, funciones y simbiosis sin alterar el contrato ni calcular.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de RE como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
    • RE no calcula C/L/K/Tru
    • material sin aprobación de dominio no debe usarse arriba
    • barrer solo vela coherencia interna de RE, no del sistema completo
  reporte:
    id: RE
    modulo: realidad
    rol: RE
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • inventario
      • reporte
      • diagnostico
      • registrar_resultado_dominio
      • ejecutar_total
      • inspeccionar
      • evaluar_universal
      • registrar_inventario
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    funciones:
      • astronomia
      • fisica
    dominios_simbiosis:
      • astronomia
      • fisica
    autoridad:
      • Descubrir FUNCION en archivos y subcarpetas de dominio
      • Velar no-contradicción y unicidad de nombres de función
      • Registrar cierre contractual de material (aprobado/rechazado)
      • Exponer estado del canal de acceso
      • Reportar inventario, reporte y diagnóstico propios
    conocimiento_exportable:
      • inventario
      • reporte
      • diagnostico
      • funciones
      • dominios_simbiosis
      • estados_material
      • contrato_simbiosis
      • acceso
    operaciones_arquitectonicas:
      ejecutar_total: True
      inspeccionar: True
      registrar_inventario: True
  diagnostico:
    id: RE
    modulo: realidad
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      • simbiosis activa: ['astronomia', 'fisica']
    recomendaciones:
      []
    coherente: True
  inventario:
    id: RE
    nombre: realidad
    rol: RE
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • inventario
      • reporte
      • diagnostico
      • registrar_resultado_dominio
      • ejecutar_total
      • inspeccionar
      • evaluar_universal
      • registrar_inventario
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    funciones:
      astronomia:
        archivo: conocimiento_humano/astronomia.py
        nombre: astronomia
        hace: Traer y etiquetar material de astronomía y astrofísica; pedir evaluación a Engine bajo el O de esta disciplina; aprobar o rechazar el material antes de que suba.
        provee:
          • material_etiquetado_astronomia
          • peticion_evaluacion_engine
          • aprobacion_dominio
        o_evaluacion: Contraste de material astronómico: observaciones, modelos celestes y datos de instrumentos. Candidato a K bajo este O; no es ancla de R.
        pide_evaluacion_engine: True
        requiere_aprobacion_dominio: True
      fisica:
        archivo: conocimiento_humano/fisica.py
        nombre: fisica
        hace: Traer y etiquetar material de física (teorías, experimentos, constantes, modelos); pedir evaluación a Engine bajo el O de esta disciplina; aprobar o rechazar el material antes de que suba.
        provee:
          • material_etiquetado_fisica
          • peticion_evaluacion_engine
          • aprobacion_dominio
        o_evaluacion: Contraste de material de física: teorías, datos experimentales y modelos. Candidato a K bajo este O; no es ancla de R.
        pide_evaluacion_engine: True
        requiere_aprobacion_dominio: True
    coherente: True
    dominios_simbiosis:
      • astronomia
      • fisica
    acceso:
      canal: acceso.Canal
      hay_requests: False
      hay_acceso: True
    contrato_simbiosis:
      quien_calcula: Engine bajo O declarado por el dominio
      quien_aprueba_material: el dominio que pidió la evaluación
      quien_vela_modulo: realidad.barrer (no-contradicción)
      material_sin_aprobacion: no sube
    funcion: Descubrir y validar dominios/funciones del módulo; sostener el contrato de simbiosis dominio↔Engine; registrar aprobación o rechazo de material; reportar estado estructural propio.
    autoridad:
      • Descubrir FUNCION en archivos y subcarpetas de dominio
      • Velar no-contradicción y unicidad de nombres de función
      • Registrar cierre contractual de material (aprobado/rechazado)
      • Exponer estado del canal de acceso
      • Reportar inventario, reporte y diagnóstico propios
    conocimiento_exportable:
      • inventario
      • reporte
      • diagnostico
      • funciones
      • dominios_simbiosis
      • estados_material
      • contrato_simbiosis
      • acceso
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
      • RE no calcula C/L/K/Tru
      • material sin aprobación de dominio no debe usarse arriba
      • barrer solo vela coherencia interna de RE, no del sistema completo

══════════════════════════════════════════════════════════════════════
  MÓDULO SF/self
══════════════════════════════════════════════════════════════════════
  id: SF
  nombre: self
  rol: SF
  version: 1.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: FASE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Yo funcional del sistema. Centro de elección e identidad de fase. Casa operativa L4. Punto de acceso a perspectivas L1…L6. Oscila entre alturas; registra actos de agency sin side-effects. No orquesta. No calcula Tru.
  funcion: Ser el punto de referencia de elección e identidad de fase: exponer quién es el sistema en fase, desde qué altura opera, en qué modo de lucidez está, registrar actos de elección, y ofrecer a Engine las perspectivas L1…L6 como mecanismos legibles para cálculo y resolución de problemas.
  no_hace:
    []
  autoridad:
    • Exponer identidad de fase (yo_funcional)
    • Reportar y cambiar altura operativa del Self (oscilar)
    • Declarar desde qué altura opera (desde_donde)
    • Clasificar modo de lucidez (estado_self)
    • Registrar actos de agency sin side-effects (elegir)
    • Declarar acceso a perspectivas L1…L6
    • Verificar coherencia interna y reportar estado propio
  conocimiento_exportable:
    • yo_funcional
    • oscilar
    • desde_donde
    • elegir
    • estado_self
    • barrer
    • verificar
    • inventario
    • reporte
    • diagnostico
  consultas_soportadas:
    • yo_funcional
    • desde_donde
    • estado_self
    • oscilar
    • elegir
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • verificar_coherencia
  requiere:
    • CE
    • AX
    • FO
    • MC
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
  capacidades:
    • verificar
    • barrer
    • verificar_salida
    • yo_funcional
    • oscilar
    • desde_donde
    • estado_self
    • elegir
    • inventario
    • reporte
    • diagnostico
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia interna de SF.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, capa_activa, modo, errores
      acceso_archivos:
        • *
    barrer:
      descripcion: Centinela de SF: identidad y estado interno.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, identidad_disponible, capa_activa, modo, errores
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Comprueba forma mínima de una salida de SF.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    yo_funcional:
      descripcion: Identidad de fase anclada en cuerpo axiomático self.
      entrada: *
      validar_esquema:
        • *
      salida: dict con capa_activa, modo, ax_self, identidad_disponible, perspectivas
      acceso_archivos:
        • *
    oscilar:
      descripcion: Cambia o reporta la altura operativa del Self (L1…L6).
      entrada: *
      validar_esquema:
        • *
      salida: dict con ok, capa_activa, altura_operativa, modo, cambio
      acceso_archivos:
        • *
    desde_donde:
      descripcion: Reporta altura y modo actuales del Self.
      entrada: *
      validar_esquema:
        • *
      salida: dict con capa_activa, altura_operativa, modo, en_casa, perspectivas
      acceso_archivos:
        • *
    estado_self:
      descripcion: Clasifica lucidez: REACTIVE|MECHANICAL|CONSCIOUS|META|INTEGRATED.
      entrada: *
      validar_esquema:
        • *
      salida: dict con modo, capa_activa, en_casa, coherente
      acceso_archivos:
        • *
    elegir:
      descripcion: Registra un acto de agency sin ejecutar efectos externos.
      entrada: *
      validar_esquema:
        • *
      salida: dict con ok, eleccion, desde, modo, n_elecciones
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario estructural del módulo SF.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, capacidades, capas_validas, modos_validos, perspectivas
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte de estado del módulo SF.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, coherente, capa_activa, modo, errores
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico: problemas, advertencias, recomendaciones.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre SF. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de SF. Expone constantes, capacidades, capas, modos y estado sin alterar el contrato ni calcular.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de SF como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • la casa operativa del Self es L4_YO
    • oscilar no es elegir
    • elegir no ejecuta efectos externos
    • las perspectivas L1…L6 son mecanismos legibles, no dependencias de arranque
    • las capacidades declaradas son callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
    • este módulo siempre puede reportar su propio estado
  reporte:
    id: SF
    modulo: self
    rol: SF
    version: 1.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: FASE
    estado: OPERATIVO
    coherente: True
    capa_activa: L4_YO
    altura_operativa: L4
    modo: CONSCIOUS
    casa: L4_YO
    identidad_disponible: True
    n_declaraciones_self: 22
    n_oscilaciones: 0
    n_elecciones: 0
    errores:
      []
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • yo_funcional
      • oscilar
      • desde_donde
      • estado_self
      • elegir
      • inventario
      • reporte
      • diagnostico
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    operaciones_arquitectonicas:
      ejecutar_total: True
      inspeccionar: True
      registrar_inventario: True
  diagnostico:
    id: SF
    modulo: self
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      • SF coherente
    coherente: True
    capa_activa: L4_YO
    modo: CONSCIOUS
    identidad_disponible: True
  inventario:
    id: SF
    nombre: self
    rol: SF
    version: 1.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: FASE
    compatible_desde: 1.0
    api_engine: >=1.0
    casa: L4_YO
    capa_activa: L4_YO
    modo: CONSCIOUS
    capacidades:
      • barrer
      • desde_donde
      • diagnostico
      • ejecutar_total
      • elegir
      • estado_self
      • evaluar_universal
      • inspeccionar
      • inventario
      • oscilar
      • registrar_inventario
      • reporte
      • verificar
      • verificar_salida
      • yo_funcional
    capas_validas:
      • L1_CUERPO
      • L2_EGO
      • L3_MENTE
      • L4_YO
      • L5_CONSCIENCIA
      • L6_ALMA
    modos_validos:
      • CONSCIOUS
      • INTEGRATED
      • MECHANICAL
      • META
      • REACTIVE
    perspectivas:
      • L1_CUERPO
      • L2_EGO
      • L3_MENTE
      • L4_YO
      • L5_CONSCIENCIA
      • L6_ALMA
    n_oscilaciones: 0
    n_elecciones: 0
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • la casa operativa del Self es L4_YO
      • oscilar no es elegir
      • elegir no ejecuta efectos externos
      • las perspectivas L1…L6 son mecanismos legibles, no dependencias de arranque
      • las capacidades declaradas son callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
      • este módulo siempre puede reportar su propio estado

══════════════════════════════════════════════════════════════════════
  MÓDULO SC/spartaco_seguridad
══════════════════════════════════════════════════════════════════════
  id: SC
  nombre: spartaco_seguridad
  rol: SC
  version: 1.7
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Adaptador Spartaco (SC). Mantiene sincronizado el catálogo con el estado real del árbol de directorios.
  funcion: Mantener sincronizado el catálogo del módulo con el estado real del árbol de directorios.
  no_hace:
    • No implementa la lógica de los archivos del árbol
    • No calcula C/L/K/Tru
    • No orquesta ciclos
    • No define vocabulario fijo de conceptos de seguridad
  autoridad:
    • Sincronizar el catálogo con el árbol
    • Exponer recursos y conceptos descubiertos
    • Reportar el estado estructural del módulo
  conocimiento_exportable:
    • inventario
    • reporte
    • diagnostico
    • catalogo
    • conceptos
  consultas_soportadas:
    • verificar
    • barrer
    • inventario
    • reporte
    • diagnostico
    • catalogo
    • verificar_salida
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
  capacidades:
    • verificar
    • barrer
    • verificar_salida
    • inventario
    • reporte
    • diagnostico
    • catalogo
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Garantiza la coherencia del catálogo sincronizado.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, errores, choques, recursos
      acceso_archivos:
        • *
    barrer:
      descripcion: Sincroniza el árbol y reporta coherencia.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, recursos, conceptos
      acceso_archivos:
        • *
    inventario:
      descripcion: Garantiza la enumeración de recursos y conceptos.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, version, recursos, conceptos
      acceso_archivos:
        • *
    reporte:
      descripcion: Garantiza el estado actual del módulo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, version, recursos
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Garantiza problemas y advertencias del catálogo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias
      acceso_archivos:
        • *
    catalogo:
      descripcion: Recursos y conceptos descubiertos en el árbol.
      entrada: *
      validar_esquema:
        • *
      salida: dict con n, recursos, conceptos
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Forma mínima de una salida del módulo.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre SC. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de SC. Expone constantes, capacidades, catálogo y estado sin alterar el contrato ni calcular.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de SC como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
    • este archivo no ejecuta la lógica del árbol
    • el catálogo refleja el árbol en tiempo de ejecución
    • los conceptos de seguridad los declaran los recursos, no el adaptador
  reporte:
    id: SC
    modulo: spartaco_seguridad
    nombre: spartaco_seguridad
    rol: SC
    version: 1.7
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • inventario
      • reporte
      • diagnostico
      • catalogo
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • CT
    recursos:
      • CAPACIDADES
      • PROTECCION
    conceptos:
      • ALTERACIÓN
      • CÓDIGO_COMPROMETIDO
      • CÓDIGO_INVÁLIDO
      • FIRMA_INVÁLIDA
      • INTEGRIDAD_COMPROMETIDA
      • MANIFIESTO_AUSENTE
      • MANIPULACIÓN
      • VERSIÓN_REGRESIVA
    total_validos: 2
    errores:
      []
    choques:
      []
  diagnostico:
    id: SC
    modulo: spartaco_seguridad
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    salud: True
  inventario:
    id: SC
    nombre: spartaco_seguridad
    rol: SC
    version: 1.7
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • inventario
      • reporte
      • diagnostico
      • catalogo
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • CT
    autoridad:
      • Sincronizar el catálogo con el árbol
      • Exponer recursos y conceptos descubiertos
      • Reportar el estado estructural del módulo
    conocimiento_exportable:
      • inventario
      • reporte
      • diagnostico
      • catalogo
      • conceptos
    consultas_soportadas:
      • verificar
      • barrer
      • inventario
      • reporte
      • diagnostico
      • catalogo
      • verificar_salida
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
      • este archivo no ejecuta la lógica del árbol
      • el catálogo refleja el árbol en tiempo de ejecución
      • los conceptos de seguridad los declaran los recursos, no el adaptador
    recursos:
      CAPACIDADES:
        ruta: capacidades.py
        nombre: capacidades
        hace: Reporta las capacidades declaradas por cada recurso del árbol (incluido este) y el estado estructural de cada una: existe y es callable. Cuantifica exacto. No elimina evidencia. No ejecuta.
        herramienta: Introspección hasattr + callable sobre los recursos descubiertos
        version: 1.3
        clave_declaracion: capacidades_recurso
        capacidades_recurso:
          • auditar
          • capacidades_de
          • resumen
          • tabla
        conceptos:
          • CÓDIGO_INVÁLIDO
        no_hace:
          • No ejecuta capacidades auditadas
          • No infiere capacidades de dir() ni de __all__
          • No modifica recursos, adaptador ni Engine
          • No convierte ausencia de declaración en error
          • No descarta elementos inválidos de la declaración
          • No oculta archivos sin SEGURIDAD
      PROTECCION:
        ruta: proteccion.py
        nombre: proteccion
        hace: Autentica artefactos con identidad genealógica: nucleo, canales S/Q, valuaciones y árbol ZSQ con node_id/parent_id; autoridad Ed25519.
        herramienta: Ed25519 + SHA-256 + NodoZSQ(id) + manifiesto {cuerpo, firma}
        version: 1.0
        clave_declaracion: capacidades_recurso
        capacidades_recurso:
          • nucleo
          • nucleo_digest
          • canales
          • z_invariante
          • comparar_z
          • node_id
          • construir_arbol
          • NodoZSQ
          • sellar
          • verificar_neutro
          • generar_claves
          • firmar
          • firmar_bytes
          • verificar_firma
          • verificar_bytes
          • serializar
          • serializar_seguro
          • construir_cuerpo
          • construir_manifiesto
          • verificar_manifiesto
          • build
          • verificar
        conceptos:
          • FIRMA_INVÁLIDA
          • INTEGRIDAD_COMPROMETIDA
          • MANIFIESTO_AUSENTE
          • CÓDIGO_INVÁLIDO
          • VERSIÓN_REGRESIVA
          • ALTERACIÓN
          • MANIPULACIÓN
          • CÓDIGO_COMPROMETIDO
    conceptos:
      • ALTERACIÓN
      • CÓDIGO_COMPROMETIDO
      • CÓDIGO_INVÁLIDO
      • FIRMA_INVÁLIDA
      • INTEGRIDAD_COMPROMETIDA
      • MANIFIESTO_AUSENTE
      • MANIPULACIÓN
      • VERSIÓN_REGRESIVA
    total_validos: 2
    archivos:
      • capacidades.py
      • proteccion.py
    coherente: True

══════════════════════════════════════════════════════════════════════
  MÓDULO TX/taxonomia
══════════════════════════════════════════════════════════════════════
  id: TX
  nombre: taxonomia
  rol: TX
  version: 2.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Taxonomía metodológica (TX). Reglas deterministas de estructura para medir tácticas (T1–T15). Sin interpretación. No calcula Tru_total. El init audita cada táctica; si no pasa el filtro, no sale. Engine aplica esta taxonomía sobre un O_context cuando el contrato y la correlación mecánica lo autorizan.
  funcion: Auditar declaraciones de táctica; filtrar las inválidas; aplicar coincidencia estructural determinista; reportar estado propio del catálogo TX.
  no_hace:
    • No interpreta contenido semántico libre
    • No calcula C, L, K, Tru_Ri ni Tru_total
    • No orquesta el ciclo del sistema
    • No deposita reportes en Diagnóstico
    • No aplica tácticas que no pasaron el filtro interno
  autoridad:
    • Declarar y filtrar tácticas metodológicas por estructura
    • Detectar id/nombre duplicados entre archivos
    • Aplicar coincidencia estructural sobre una descripción
    • Reportar inventario, reporte y diagnóstico propios
  conocimiento_exportable:
    • inventario
    • reporte
    • diagnostico
    • tacticas
    • axiomas
  consultas_soportadas:
    • verificar
    • barrer
    • verificar_salida
    • aplicar
    • axiomas
    • inventario
    • reporte
    • diagnostico
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    evaluar_universal: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
  capacidades:
    • verificar
    • barrer
    • verificar_salida
    • aplicar
    • axiomas
    • inventario
    • reporte
    • diagnostico
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Coherencia interna de TX (alias de barrer).
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, choques, errores, tacticas
      acceso_archivos:
        • *
    barrer:
      descripcion: Audita tácticas, detecta choques y filtra inválidas.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, choques, errores, tacticas, total_declaradas, total_validas, notas
      acceso_archivos:
        • *
    aplicar:
      descripcion: Aplica coincidencia estructural de tácticas válidas sobre una descripción. No calcula Tru.
      entrada: *
      validar_esquema:
        • *
      salida: dict con aplicadas, total, tacticas_disponibles, O_context
      acceso_archivos:
        • *
    inventario:
      descripcion: Enumeración de tácticas que pasaron el filtro.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, version, tacticas, total_validas
      acceso_archivos:
        • *
    reporte:
      descripcion: Estado actual del módulo TX.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, version, capacidades, coherente
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Problemas, advertencias y recomendaciones de TX.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    axiomas:
      descripcion: Declaraciones axiomáticas del oficio TX.
      entrada: *
      validar_esquema:
        • *
      salida: lista de dicts axiomáticos
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Forma mínima de una salida de TX.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre TX. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de TX. Expone constantes, capacidades, tacticas y estado sin alterar el contrato ni calcular.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de TX como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
    • TX no calcula Tru_total
    • solo tácticas que pasan el filtro se aplican
    • medición por estructura explícita, no por interpretación
  reporte:
    id: TX
    modulo: taxonomia
    rol: TX
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • aplicar
      • axiomas
      • inventario
      • reporte
      • diagnostico
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    tacticas:
      • T1
      • T10
      • T11
      • T12
      • T13
      • T14
      • T15
      • T2
      • T3
      • T4
      • T5
      • T6
      • T7
      • T8
      • T9
    total_validas: 15
    autoridad:
      • Declarar y filtrar tácticas metodológicas por estructura
      • Detectar id/nombre duplicados entre archivos
      • Aplicar coincidencia estructural sobre una descripción
      • Reportar inventario, reporte y diagnóstico propios
    conocimiento_exportable:
      • inventario
      • reporte
      • diagnostico
      • tacticas
      • axiomas
    operaciones_arquitectonicas:
      ejecutar_total: True
      inspeccionar: True
      registrar_inventario: True
  diagnostico:
    id: TX
    modulo: taxonomia
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    coherente: True
  inventario:
    id: TX
    nombre: taxonomia
    rol: TX
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • aplicar
      • axiomas
      • inventario
      • reporte
      • diagnostico
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    tacticas:
      T1:
        nombre: Concession-pivot
        degrada:
          • C
          • K
      T2:
        nombre: False Deference
        degrada:
          • C
          • K
      T3:
        nombre: False Choice
        degrada:
          • K
          • L
      T4:
        nombre: Pseudo-rigor
        degrada:
          • K
      T5:
        nombre: Object Invention
        degrada:
          • A
          • K
          • C
      T6:
        nombre: Seeded Doubt
        degrada:
          • K
          • L
      T7:
        nombre: Usurped Verdict
        degrada:
          • K
      T8:
        nombre: Methodological Drift
        degrada:
          • L
          • K
      T9:
        nombre: Authority Label
        degrada:
          • K
      T10:
        nombre: Equivocation
        degrada:
          • L
          • C
      T11:
        nombre: Moving the Goalposts
        degrada:
          • L
          • K
      T12:
        nombre: Hedging
        degrada:
          • L
          • K
      T13:
        nombre: Category Mistake
        degrada:
          • L
          • K
      T14:
        nombre: Ad Hoc Hypothesis
        degrada:
          • L
          • K
      T15:
        nombre: Bucle de inversion de objetos
        degrada:
          • A
          • K
          • L
    total_validas: 15
    funcion: Auditar declaraciones de táctica; filtrar las inválidas; aplicar coincidencia estructural determinista; reportar estado propio del catálogo TX.
    autoridad:
      • Declarar y filtrar tácticas metodológicas por estructura
      • Detectar id/nombre duplicados entre archivos
      • Aplicar coincidencia estructural sobre una descripción
      • Reportar inventario, reporte y diagnóstico propios
    conocimiento_exportable:
      • inventario
      • reporte
      • diagnostico
      • tacticas
      • axiomas
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • las capacidades declaradas son siempre callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
      • TX no calcula Tru_total
      • solo tácticas que pasan el filtro se aplican
      • medición por estructura explícita, no por interpretación

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
    • verificar_coherencia
    • listar_categorias
    • resolver_pedido
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • VX
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
    evaluar_universal: True
  capacidades:
    • verificar
    • barrer
    • verificar_salida
    • categorias
    • capacidades
    • resolver_pedido
    • inventario
    • reporte
    • diagnostico
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Alias de barrer. Verifica coherencia del catálogo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, categorias, ids, errores
      acceso_archivos:
        • *
    barrer:
      descripcion: Evalúa coherencia del catálogo. No calcula Tru.
      entrada: *
      validar_esquema:
        • *
      salida: dict con coherente, categorias, ids, errores, version
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario completo del módulo y del catálogo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, version, capacidades, extension
      acceso_archivos:
        • *
    capacidades:
      descripcion: Vista explícita del catálogo para Engine/Omega.
      entrada: *
      validar_esquema:
        • *
      salida: dict con categorias resumidas, total, coherente
      acceso_archivos:
        • *
    categorias:
      descripcion: Lista del catálogo si coherente; si no, lista vacía.
      entrada: *
      validar_esquema:
        • *
      salida: list[dict] de categorías normalizadas
      acceso_archivos:
        • *
    resolver_pedido:
      descripcion: Normaliza un pedido de Omega/Engine a una categoría. No calcula. No orquesta.
      entrada: *
      validar_esquema:
        • *
      salida: dict con ok, categoria, unidad, factores_evaluables, ...
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte interno de estado del módulo TT.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, coherente, categorias, errores
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico: qué falta o está mal en el catálogo.
      entrada: *
      validar_esquema:
        • *
      salida: dict con estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Comprueba si una salida de barrer o resolver es válida.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre TT. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de TT. Expone constantes, capacidades, catalogo y estado sin alterar el contrato ni calcular.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de TT como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
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
      • verificar_salida
      • categorias
      • capacidades
      • resolver_pedido
      • inventario
      • reporte
      • diagnostico
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • SC
      • CT
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
      • verificar_coherencia
      • listar_categorias
      • resolver_pedido
      • obtener_inventario
      • obtener_reporte
      • obtener_diagnostico
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
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
      • verificar_salida
      • categorias
      • capacidades
      • resolver_pedido
      • inventario
      • reporte
      • diagnostico
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
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
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • SC
      • CT
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
  MÓDULO VX/verificacion
══════════════════════════════════════════════════════════════════════
  id: VX
  nombre: verificacion
  rol: VX
  version: 2.0
  version_contrato: 1.0
  esquema: VPSI-CONTRACT-1.0
  estabilidad: ESTABLE
  compatible_desde: 1.0
  api_engine: >=1.0
  descripcion: Autoridad exclusiva de verificación estructural. Determina si una estructura satisface o viola un conjunto de reglas formales. Jurisdicción: código, contratos, módulos, configuraciones, salidas, estructuras, grafos y futuras representaciones. Solo produce evidencia verificable. No interpreta, no calcula Tru, no decide, no corrige, no modifica, no ejecuta. No sustituye a AX ni a Diagnóstico.
  funcion: Contrastar estructuras contra reglas formales y generar evidencia de verificación. El algoritmo operativo actual usa AuditorAxiomatico sobre código; la responsabilidad del módulo admite cualquier estructura formal sin cambiar la API.
  no_hace:
    • No interpreta intención
    • No calcula C
    • No calcula L
    • No calcula K
    • No calcula Tru
    • No modifica estructuras auditadas
    • No corrige implementaciones
    • No toma decisiones
    • No ejecuta acciones
    • No deposita en Diagnóstico
    • No sustituye a AX
    • No sustituye a Diagnóstico
    • No declara conocimiento axiomático oficial
  autoridad:
    • Verificar estructuras
    • Contrastar estructuras contra reglas formales
    • Reportar inconsistencias estructurales
    • Generar evidencia de verificación
    • Reportar su estado
    • Reportar inventario
    • Reportar diagnóstico propio
  conocimiento_exportable:
    • verificar
    • barrer
    • inventario
    • reporte
    • diagnostico
    • verificar_salida
    • axiomas
    • evidencia
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  consultas_soportadas:
    • verificar_estructura
    • barrer
    • verificar_salida
    • obtener_inventario
    • obtener_reporte
    • obtener_diagnostico
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
  requiere:
    • CE
    • AX
    • FO
    • MC
    • SF
    • CA
    • CX
    • DI
    • RE
    • TX
    • CH
    • CIT
    • DGCO
    • UI
    • CC
    • TT
    • SC
    • CT
  autoriza_engine:
    leer: True
    ejecutar: True
    consultar: True
    recombinar: True
    reportar: True
    auditar: True
    inventariar: True
    alterar: False
    crear: True
    actualizar: False
    validar: True
    procesar: True
    analizar: True
    generar: True
    exportar: True
    importar: True
    respaldar: True
    recuperar: True
    sincronizar: True
    monitorear: True
    metricas: True
    diagnostico: True
    estado: True
    version: True
    salud: True
    inventario: True
    capacidades: True
    errores: True
    advertencias: True
    dependencias: True
    contrato: True
    conocimiento: True
    reporte: True
    validar_esquema: True
    acceso_archivos: True
    evaluar_universal: True
    ejecutar_total: True
    inspeccionar: True
    registrar_inventario: True
  capacidades:
    • verificar
    • barrer
    • verificar_salida
    • axiomas
    • inventario
    • reporte
    • diagnostico
    • ejecutar_total
    • inspeccionar
    • registrar_inventario
    • evaluar_universal
  capacidades_meta:
    verificar:
      descripcion: Verifica una estructura contra reglas formales. Produce evidencia. No interpreta ni corrige.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, coherente, errores, evidencia, detalle
      acceso_archivos:
        • *
    barrer:
      descripcion: Alias de verificar. Centinela de coherencia estructural.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, coherente, errores, evidencia, detalle
      acceso_archivos:
        • *
    inventario:
      descripcion: Inventario contractual del módulo VX.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, nombre, rol, version, version_contrato, esquema, estabilidad, capacidades, jurisdiccion
      acceso_archivos:
        • *
    reporte:
      descripcion: Reporte interno de estado de VX.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, estado, coherente, capacidades, jurisdiccion
      acceso_archivos:
        • *
    diagnostico:
      descripcion: Diagnóstico propio de VX. No consulta DiagnosticoGlobal.
      entrada: *
      validar_esquema:
        • *
      salida: dict con id, estado, problemas, advertencias, recomendaciones
      acceso_archivos:
        • *
    verificar_salida:
      descripcion: Comprueba forma mínima de una salida de VX.
      entrada: *
      validar_esquema:
        • *
      salida: bool
      acceso_archivos:
        • *
    axiomas:
      descripcion: Alias temporal de compatibilidad. AX es la única autoridad del conocimiento. No declara corpus oficial.
      entrada: *
      validar_esquema:
        • *
      salida: list vacía (conocimiento oficial en AX)
      acceso_archivos:
        • *
    ejecutar_total:
      descripcion: Autoridad total de ENGINE sobre VX. Ejerce TODAS las unidades operativamente ejecutables del módulo conforme a su contrato e inventario. Todo es callable real. No inventa capacidades.
      entrada: peticion opcional (dict)
      validar_esquema:
        • *
      salida: dict con resultados de todas las unidades ejecutadas
      acceso_archivos:
        • *
    inspeccionar:
      descripcion: Capacidad meta de inspeccion estructural de VX. Expone constantes, capacidades y estado sin alterar el contrato ni calcular.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con estructura, capacidades y estado del modulo
      acceso_archivos:
        • acceso_archivos
    registrar_inventario:
      descripcion: Registra el inventario estructural de VX como instantanea determinista. No altera evidencia.
      entrada: peticion opcional (dict)
      validar_esquema:
        • acceso_archivos
      salida: dict con inventario registrado
      acceso_archivos:
        • acceso_archivos
    evaluar_universal:
      descripcion: Evalúa las capacidades reales de este módulo cuya firma se satisfaga con los hechos de entrada. Engine entrega la entrada; este callable solo aplica lo local.
      entrada: hechos: dict
      validar_esquema:
        • *
      salida: dict con hechos, traza, ejecutadas
      acceso_archivos:
        • *
  estados_validos:
    • NO_INICIADO
    • OPERATIVO
    • DEGRADADO
    • RECHAZADO
  invariantes:
    • el id del módulo nunca cambia
    • el rol nunca cambia
    • VX nunca modifica la estructura auditada
    • VX nunca corrige evidencia
    • VX nunca interpreta intención
    • VX nunca calcula métricas de verdad (C/L/K/Tru)
    • VX solo produce evidencia verificable
    • VX no deposita en Diagnóstico; Engine decide el destino de la evidencia
    • VX no declara conocimiento axiomático oficial (AX es la autoridad)
    • las capacidades declaradas son callables tras la resolución
    • este módulo no modifica el estado de otros módulos
    • este módulo no inventa capacidades no declaradas en CONTENEDOR
    • este módulo siempre puede reportar su propio estado
    • inventario() siempre incluye id, nombre, rol, version del CONTENEDOR
  reporte:
    id: VX
    nombre: verificacion
    rol: VX
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    estado: OPERATIVO
    coherente: True
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • axiomas
      • inventario
      • reporte
      • diagnostico
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    jurisdiccion:
      • codigo
      • contratos
      • modulos
      • configuraciones
      • salidas
      • estructuras
      • grafos
      • arboles
      • futuras_representaciones
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    operaciones_arquitectonicas:
      ejecutar_total: True
      inspeccionar: True
      registrar_inventario: True
    nota: VX no mantiene sesión de auditoría persistente. Cada verificar()/barrer() produce evidencia puntual.
  diagnostico:
    id: VX
    nombre: verificacion
    rol: VX
    estado: OPERATIVO
    problemas:
      []
    advertencias:
      []
    recomendaciones:
      []
    coherente: True
    nota: Diagnóstico propio de VX. La evidencia de verificaciones concretas se obtiene invocando verificar()/barrer(); Engine decide su destino.
  inventario:
    id: VX
    nombre: verificacion
    rol: VX
    version: 2.0
    version_contrato: 1.0
    esquema: VPSI-CONTRACT-1.0
    estabilidad: ESTABLE
    compatible_desde: 1.0
    api_engine: >=1.0
    capacidades:
      • verificar
      • barrer
      • verificar_salida
      • axiomas
      • inventario
      • reporte
      • diagnostico
      • ejecutar_total
      • inspeccionar
      • registrar_inventario
      • evaluar_universal
    funcion: Autoridad de verificación estructural. Determina si una estructura satisface o viola reglas formales. Solo produce evidencia. No interpreta, no corrige, no ejecuta.
    jurisdiccion:
      • codigo
      • contratos
      • modulos
      • configuraciones
      • salidas
      • estructuras
      • grafos
      • arboles
      • futuras_representaciones
    requiere:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    invariantes:
      • el id del módulo nunca cambia
      • el rol nunca cambia
      • VX nunca modifica la estructura auditada
      • VX nunca corrige evidencia
      • VX nunca interpreta intención
      • VX nunca calcula métricas de verdad (C/L/K/Tru)
      • VX solo produce evidencia verificable
      • VX no deposita en Diagnóstico; Engine decide el destino de la evidencia
      • VX no declara conocimiento axiomático oficial (AX es la autoridad)
      • las capacidades declaradas son callables tras la resolución
      • este módulo no modifica el estado de otros módulos
      • este módulo no inventa capacidades no declaradas en CONTENEDOR
      • este módulo siempre puede reportar su propio estado
      • inventario() siempre incluye id, nombre, rol, version del CONTENEDOR

══════════════════════════════════════════════════════════════════════
  DEPENDENCIAS
══════════════════════════════════════════════════════════════════════
  grafo:
    axiomas:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
    cache:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    calculator:
      • CT
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
    capacidades_engine:
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
    catalogo_citaciones:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • TT
      • SC
    citacion:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    constante:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
    contexto:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    correlacion_mecanica:
      • CE
      • AX
      • FO
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    diagnosticoD:
      • AX
      • CA
      • CC
      • CE
      • CH
      • CIT
      • CT
      • CX
      • DGCO
      • DI
      • FO
      • MC
      • RE
      • SC
      • SF
      • TT
      • TX
      • UI
      • VX
      • axiomas
      • cache
      • calculator
      • capacidades_engine
      • catalogo_citaciones
      • citacion
      • constante
      • contexto
      • correlacion_mecanica
      • diccionario
      • formulas
      • interfaz
      • realidad
      • self
      • spartaco_seguridad
      • taxonomia
      • tru_totales
      • verificacion
    diccionario:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    formulas:
      • CE
      • AX
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    interfaz:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • CC
      • TT
      • SC
      • CT
    realidad:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    self:
      • CE
      • AX
      • FO
      • MC
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    spartaco_seguridad:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • CT
    taxonomia:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
    tru_totales:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • VX
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • SC
      • CT
    verificacion:
      • CE
      • AX
      • FO
      • MC
      • SF
      • CA
      • CX
      • DI
      • RE
      • TX
      • CH
      • CIT
      • DGCO
      • UI
      • CC
      • TT
      • SC
      • CT
  faltantes:
  orden_topologico:
    • axiomas
    • cache
    • calculator
    • capacidades_engine
    • catalogo_citaciones
    • citacion
    • constante
    • contexto
    • correlacion_mecanica
    • diagnosticoD
    • diccionario
    • formulas
    • interfaz
    • realidad
    • self
    • spartaco_seguridad
    • taxonomia
    • tru_totales
    • verificacion
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
      id: axiomas.limite_axiomático
      nombre: limite_axiomático
      tipo: capacidad
      modulo: axiomas
    [15]
      id: axiomas.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: axiomas
    [16]
      id: axiomas.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: axiomas
    [17]
      id: axiomas.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: axiomas
    [18]
      id: CH
      nombre: cache
      rol: CH
      tipo: modulo
    [19]
      id: cache.verificar
      nombre: verificar
      tipo: capacidad
      modulo: cache
    [20]
      id: cache.barrer
      nombre: barrer
      tipo: capacidad
      modulo: cache
    [21]
      id: cache.depositar
      nombre: depositar
      tipo: capacidad
      modulo: cache
    [22]
      id: cache.leer
      nombre: leer
      tipo: capacidad
      modulo: cache
    [23]
      id: cache.leer_eventos
      nombre: leer_eventos
      tipo: capacidad
      modulo: cache
    [24]
      id: cache.leer_por_ciclo
      nombre: leer_por_ciclo
      tipo: capacidad
      modulo: cache
    [25]
      id: cache.leer_por_modulo
      nombre: leer_por_modulo
      tipo: capacidad
      modulo: cache
    [26]
      id: cache.leer_por_tipo
      nombre: leer_por_tipo
      tipo: capacidad
      modulo: cache
    [27]
      id: cache.leer_por_categoria
      nombre: leer_por_categoria
      tipo: capacidad
      modulo: cache
    [28]
      id: cache.leer_por_capacidad
      nombre: leer_por_capacidad
      tipo: capacidad
      modulo: cache
    [29]
      id: cache.leer_por_origen
      nombre: leer_por_origen
      tipo: capacidad
      modulo: cache
    [30]
      id: cache.leer_por_destino
      nombre: leer_por_destino
      tipo: capacidad
      modulo: cache
    [31]
      id: cache.leer_por_estado
      nombre: leer_por_estado
      tipo: capacidad
      modulo: cache
    [32]
      id: cache.leer_por_seq
      nombre: leer_por_seq
      tipo: capacidad
      modulo: cache
    [33]
      id: cache.leer_por_timestamp
      nombre: leer_por_timestamp
      tipo: capacidad
      modulo: cache
    [34]
      id: cache.categorias
      nombre: categorias
      tipo: capacidad
      modulo: cache
    [35]
      id: cache.inventario
      nombre: inventario
      tipo: capacidad
      modulo: cache
    [36]
      id: cache.reporte
      nombre: reporte
      tipo: capacidad
      modulo: cache
    [37]
      id: cache.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: cache
    [38]
      id: cache.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: cache
    [39]
      id: cache.backend_para_centinela
      nombre: backend_para_centinela
      tipo: capacidad
      modulo: cache
    [40]
      id: cache.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: cache
    [41]
      id: cache.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: cache
    [42]
      id: cache.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: cache
    [43]
      id: cache.mapear_codigo
      nombre: mapear_codigo
      tipo: capacidad
      modulo: cache
    [44]
      id: cache.clasificar_ids
      nombre: clasificar_ids
      tipo: capacidad
      modulo: cache
    [45]
      id: cache.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: cache
    [46]
      id: CA
      nombre: calculator
      rol: CA
      tipo: modulo
    [47]
      id: calculator.calcular
      nombre: calcular
      tipo: capacidad
      modulo: calculator
    [48]
      id: calculator.calcular_C
      nombre: calcular_C
      tipo: capacidad
      modulo: calculator
    [49]
      id: calculator.calcular_L
      nombre: calcular_L
      tipo: capacidad
      modulo: calculator
    [50]
      id: calculator.calcular_K
      nombre: calcular_K
      tipo: capacidad
      modulo: calculator
    [51]
      id: calculator.calcular_factor
      nombre: calcular_factor
      tipo: capacidad
      modulo: calculator
    [52]
      id: calculator.representar
      nombre: representar
      tipo: capacidad
      modulo: calculator
    [53]
      id: calculator.validar_evidencia
      nombre: validar_evidencia
      tipo: capacidad
      modulo: calculator
    [54]
      id: calculator.explicar_calculo
      nombre: explicar_calculo
      tipo: capacidad
      modulo: calculator
    [55]
      id: calculator.verificar
      nombre: verificar
      tipo: capacidad
      modulo: calculator
    [56]
      id: calculator.barrer
      nombre: barrer
      tipo: capacidad
      modulo: calculator
    [57]
      id: calculator.inventario
      nombre: inventario
      tipo: capacidad
      modulo: calculator
    [58]
      id: calculator.reporte
      nombre: reporte
      tipo: capacidad
      modulo: calculator
    [59]
      id: calculator.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: calculator
    [60]
      id: calculator.leer_ids_escala
      nombre: leer_ids_escala
      tipo: capacidad
      modulo: calculator
    [61]
      id: calculator.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: calculator
    [62]
      id: calculator.historial
      nombre: historial
      tipo: capacidad
      modulo: calculator
    [63]
      id: calculator.verificar_calculo_de_C_L_K
      nombre: verificar_calculo_de_C_L_K
      tipo: capacidad
      modulo: calculator
    [64]
      id: calculator.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: calculator
    [65]
      id: calculator.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: calculator
    [66]
      id: calculator.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: calculator
    [67]
      id: calculator.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: calculator
    [68]
      id: CE
      nombre: capacidades_engine
      rol: CE
      tipo: modulo
    [69]
      id: capacidades_engine.verificar
      nombre: verificar
      tipo: capacidad
      modulo: capacidades_engine
    [70]
      id: capacidades_engine.barrer
      nombre: barrer
      tipo: capacidad
      modulo: capacidades_engine
    [71]
      id: capacidades_engine.inventario
      nombre: inventario
      tipo: capacidad
      modulo: capacidades_engine
    [72]
      id: capacidades_engine.skills
      nombre: skills
      tipo: capacidad
      modulo: capacidades_engine
    [73]
      id: capacidades_engine.ids
      nombre: ids
      tipo: capacidad
      modulo: capacidades_engine
    [74]
      id: capacidades_engine.por_id
      nombre: por_id
      tipo: capacidad
      modulo: capacidades_engine
    [75]
      id: capacidades_engine.listar_archivos
      nombre: listar_archivos
      tipo: capacidad
      modulo: capacidades_engine
    [76]
      id: capacidades_engine.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: capacidades_engine
    [77]
      id: capacidades_engine.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: capacidades_engine
    [78]
      id: capacidades_engine.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: capacidades_engine
    [79]
      id: capacidades_engine.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: capacidades_engine
    [80]
      id: capacidades_engine.reporte
      nombre: reporte
      tipo: capacidad
      modulo: capacidades_engine
    [81]
      id: capacidades_engine.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: capacidades_engine
    [82]
      id: capacidades_engine.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: capacidades_engine
    [83]
      id: CC
      nombre: catalogo_citaciones
      rol: CC
      tipo: modulo
    [84]
      id: catalogo_citaciones.verificar
      nombre: verificar
      tipo: capacidad
      modulo: catalogo_citaciones
    [85]
      id: catalogo_citaciones.barrer
      nombre: barrer
      tipo: capacidad
      modulo: catalogo_citaciones
    [86]
      id: catalogo_citaciones.inventario
      nombre: inventario
      tipo: capacidad
      modulo: catalogo_citaciones
    [87]
      id: catalogo_citaciones.categorias
      nombre: categorias
      tipo: capacidad
      modulo: catalogo_citaciones
    [88]
      id: catalogo_citaciones.por_id
      nombre: por_id
      tipo: capacidad
      modulo: catalogo_citaciones
    [89]
      id: catalogo_citaciones.ids
      nombre: ids
      tipo: capacidad
      modulo: catalogo_citaciones
    [90]
      id: catalogo_citaciones.esquema
      nombre: esquema
      tipo: capacidad
      modulo: catalogo_citaciones
    [91]
      id: catalogo_citaciones.reporte
      nombre: reporte
      tipo: capacidad
      modulo: catalogo_citaciones
    [92]
      id: catalogo_citaciones.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: catalogo_citaciones
    [93]
      id: catalogo_citaciones.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: catalogo_citaciones
    [94]
      id: catalogo_citaciones.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: catalogo_citaciones
    [95]
      id: catalogo_citaciones.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: catalogo_citaciones
    [96]
      id: catalogo_citaciones.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: catalogo_citaciones
    [97]
      id: catalogo_citaciones.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: catalogo_citaciones
    [98]
      id: CIT
      nombre: citacion
      rol: CIT
      tipo: modulo
    [99]
      id: citacion.verificar
      nombre: verificar
      tipo: capacidad
      modulo: citacion
    [100]
      id: citacion.barrer
      nombre: barrer
      tipo: capacidad
      modulo: citacion
    [101]
      id: citacion.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: citacion
    [102]
      id: citacion.inventario
      nombre: inventario
      tipo: capacidad
      modulo: citacion
    [103]
      id: citacion.reporte
      nombre: reporte
      tipo: capacidad
      modulo: citacion
    [104]
      id: citacion.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: citacion
    [105]
      id: citacion.anunciar
      nombre: anunciar
      tipo: capacidad
      modulo: citacion
    [106]
      id: citacion.anunciar_todo
      nombre: anunciar_todo
      tipo: capacidad
      modulo: citacion
    [107]
      id: citacion.citar
      nombre: citar
      tipo: capacidad
      modulo: citacion
    [108]
      id: citacion.registrar
      nombre: registrar
      tipo: capacidad
      modulo: citacion
    [109]
      id: citacion.resolver
      nombre: resolver
      tipo: capacidad
      modulo: citacion
    [110]
      id: citacion.resolver_enunciado
      nombre: resolver_enunciado
      tipo: capacidad
      modulo: citacion
    [111]
      id: citacion.buscar
      nombre: buscar
      tipo: capacidad
      modulo: citacion
    [112]
      id: citacion.cadena
      nombre: cadena
      tipo: capacidad
      modulo: citacion
    [113]
      id: citacion.explicar
      nombre: explicar
      tipo: capacidad
      modulo: citacion
    [114]
      id: citacion.relacionar
      nombre: relacionar
      tipo: capacidad
      modulo: citacion
    [115]
      id: citacion.limpiar_ciclo
      nombre: limpiar_ciclo
      tipo: capacidad
      modulo: citacion
    [116]
      id: citacion.evaluar
      nombre: evaluar
      tipo: capacidad
      modulo: citacion
    [117]
      id: citacion.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: citacion
    [118]
      id: citacion.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: citacion
    [119]
      id: citacion.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: citacion
    [120]
      id: citacion.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: citacion
    [121]
      id: CT
      nombre: constante
      rol: CT
      tipo: modulo
    [122]
      id: constante.alpha
      nombre: alpha
      tipo: capacidad
      modulo: constante
    [123]
      id: constante.beta
      nombre: beta
      tipo: capacidad
      modulo: constante
    [124]
      id: constante.buscar_constante
      nombre: buscar_constante
      tipo: capacidad
      modulo: constante
    [125]
      id: constante.descubrir_constantes
      nombre: descubrir_constantes
      tipo: capacidad
      modulo: constante
    [126]
      id: constante.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: constante
    [127]
      id: constante.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: constante
    [128]
      id: constante.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: constante
    [129]
      id: constante.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: constante
    [130]
      id: constante.inventario
      nombre: inventario
      tipo: capacidad
      modulo: constante
    [131]
      id: constante.listar_constantes
      nombre: listar_constantes
      tipo: capacidad
      modulo: constante
    [132]
      id: constante.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: constante
    [133]
      id: constante.reporte
      nombre: reporte
      tipo: capacidad
      modulo: constante
    [134]
      id: constante.verificar
      nombre: verificar
      tipo: capacidad
      modulo: constante
    [135]
      id: constante.verificar_constantes
      nombre: verificar_constantes
      tipo: capacidad
      modulo: constante
    [136]
      id: CX
      nombre: contexto
      rol: CX
      tipo: modulo
    [137]
      id: contexto.resolver
      nombre: resolver
      tipo: capacidad
      modulo: contexto
    [138]
      id: contexto.evaluar
      nombre: evaluar
      tipo: capacidad
      modulo: contexto
    [139]
      id: contexto.centinela
      nombre: centinela
      tipo: capacidad
      modulo: contexto
    [140]
      id: contexto.verificar
      nombre: verificar
      tipo: capacidad
      modulo: contexto
    [141]
      id: contexto.barrer
      nombre: barrer
      tipo: capacidad
      modulo: contexto
    [142]
      id: contexto.inventario
      nombre: inventario
      tipo: capacidad
      modulo: contexto
    [143]
      id: contexto.reporte
      nombre: reporte
      tipo: capacidad
      modulo: contexto
    [144]
      id: contexto.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: contexto
    [145]
      id: contexto.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: contexto
    [146]
      id: contexto.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: contexto
    [147]
      id: contexto.ejecutar
      nombre: ejecutar
      tipo: capacidad
      modulo: contexto
    [148]
      id: contexto.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: contexto
    [149]
      id: contexto.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: contexto
    [150]
      id: contexto.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: contexto
    [151]
      id: MC
      nombre: correlacion_mecanica
      rol: MC
      tipo: modulo
    [152]
      id: correlacion_mecanica.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: correlacion_mecanica
    [153]
      id: correlacion_mecanica.barrer
      nombre: barrer
      tipo: capacidad
      modulo: correlacion_mecanica
    [154]
      id: correlacion_mecanica.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: correlacion_mecanica
    [155]
      id: correlacion_mecanica.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: correlacion_mecanica
    [156]
      id: correlacion_mecanica.evaluar
      nombre: evaluar
      tipo: capacidad
      modulo: correlacion_mecanica
    [157]
      id: correlacion_mecanica.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: correlacion_mecanica
    [158]
      id: correlacion_mecanica.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: correlacion_mecanica
    [159]
      id: correlacion_mecanica.inventario
      nombre: inventario
      tipo: capacidad
      modulo: correlacion_mecanica
    [160]
      id: correlacion_mecanica.listar_mecanicas
      nombre: listar_mecanicas
      tipo: capacidad
      modulo: correlacion_mecanica
    [161]
      id: correlacion_mecanica.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: correlacion_mecanica
    [162]
      id: correlacion_mecanica.reporte
      nombre: reporte
      tipo: capacidad
      modulo: correlacion_mecanica
    [163]
      id: correlacion_mecanica.verificar
      nombre: verificar
      tipo: capacidad
      modulo: correlacion_mecanica
    [164]
      id: correlacion_mecanica.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: correlacion_mecanica
    [165]
      id: DGCO
      nombre: diagnosticoD
      rol: DGCO
      tipo: modulo
    [166]
      id: diagnosticoD.censo
      nombre: censo
      tipo: capacidad
      modulo: diagnosticoD
    [167]
      id: diagnosticoD.verificar
      nombre: verificar
      tipo: capacidad
      modulo: diagnosticoD
    [168]
      id: diagnosticoD.barrer
      nombre: barrer
      tipo: capacidad
      modulo: diagnosticoD
    [169]
      id: diagnosticoD.presentar
      nombre: presentar
      tipo: capacidad
      modulo: diagnosticoD
    [170]
      id: diagnosticoD.reportar
      nombre: reportar
      tipo: capacidad
      modulo: diagnosticoD
    [171]
      id: diagnosticoD.inventario
      nombre: inventario
      tipo: capacidad
      modulo: diagnosticoD
    [172]
      id: diagnosticoD.reporte
      nombre: reporte
      tipo: capacidad
      modulo: diagnosticoD
    [173]
      id: diagnosticoD.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: diagnosticoD
    [174]
      id: diagnosticoD.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: diagnosticoD
    [175]
      id: diagnosticoD.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: diagnosticoD
    [176]
      id: diagnosticoD.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: diagnosticoD
    [177]
      id: diagnosticoD.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: diagnosticoD
    [178]
      id: DI
      nombre: diccionario
      rol: DI
      tipo: modulo
    [179]
      id: diccionario.verificar
      nombre: verificar
      tipo: capacidad
      modulo: diccionario
    [180]
      id: diccionario.barrer
      nombre: barrer
      tipo: capacidad
      modulo: diccionario
    [181]
      id: diccionario.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: diccionario
    [182]
      id: diccionario.inventario
      nombre: inventario
      tipo: capacidad
      modulo: diccionario
    [183]
      id: diccionario.reporte
      nombre: reporte
      tipo: capacidad
      modulo: diccionario
    [184]
      id: diccionario.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: diccionario
    [185]
      id: diccionario.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: diccionario
    [186]
      id: diccionario.resolver
      nombre: resolver
      tipo: capacidad
      modulo: diccionario
    [187]
      id: diccionario.listar
      nombre: listar
      tipo: capacidad
      modulo: diccionario
    [188]
      id: diccionario.cargar
      nombre: cargar
      tipo: capacidad
      modulo: diccionario
    [189]
      id: diccionario.cargar_todos
      nombre: cargar_todos
      tipo: capacidad
      modulo: diccionario
    [190]
      id: diccionario.definir
      nombre: definir
      tipo: capacidad
      modulo: diccionario
    [191]
      id: diccionario.significado
      nombre: significado
      tipo: capacidad
      modulo: diccionario
    [192]
      id: diccionario.palabras
      nombre: palabras
      tipo: capacidad
      modulo: diccionario
    [193]
      id: diccionario.inyectar_en_peticion
      nombre: inyectar_en_peticion
      tipo: capacidad
      modulo: diccionario
    [194]
      id: diccionario.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: diccionario
    [195]
      id: diccionario.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: diccionario
    [196]
      id: diccionario.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: diccionario
    [197]
      id: diccionario.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: diccionario
    [198]
      id: FO
      nombre: formulas
      rol: FO
      tipo: modulo
    [199]
      id: formulas.verificar
      nombre: verificar
      tipo: capacidad
      modulo: formulas
    [200]
      id: formulas.barrer
      nombre: barrer
      tipo: capacidad
      modulo: formulas
    [201]
      id: formulas.evaluar
      nombre: evaluar
      tipo: capacidad
      modulo: formulas
    [202]
      id: formulas.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: formulas
    [203]
      id: formulas.inventario
      nombre: inventario
      tipo: capacidad
      modulo: formulas
    [204]
      id: formulas.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: formulas
    [205]
      id: formulas.tru_ri
      nombre: tru_ri
      tipo: capacidad
      modulo: formulas
    [206]
      id: formulas.tru_total
      nombre: tru_total
      tipo: capacidad
      modulo: formulas
    [207]
      id: formulas.reporte
      nombre: reporte
      tipo: capacidad
      modulo: formulas
    [208]
      id: formulas.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: formulas
    [209]
      id: formulas.listar_formulas
      nombre: listar_formulas
      tipo: capacidad
      modulo: formulas
    [210]
      id: formulas.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: formulas
    [211]
      id: formulas.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: formulas
    [212]
      id: formulas.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: formulas
    [213]
      id: formulas.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: formulas
    [214]
      id: UI
      nombre: interfaz
      rol: UI
      tipo: modulo
    [215]
      id: interfaz.verificar
      nombre: verificar
      tipo: capacidad
      modulo: interfaz
    [216]
      id: interfaz.barrer
      nombre: barrer
      tipo: capacidad
      modulo: interfaz
    [217]
      id: interfaz.componer
      nombre: componer
      tipo: capacidad
      modulo: interfaz
    [218]
      id: interfaz.observar
      nombre: observar
      tipo: capacidad
      modulo: interfaz
    [219]
      id: interfaz.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: interfaz
    [220]
      id: interfaz.inventario
      nombre: inventario
      tipo: capacidad
      modulo: interfaz
    [221]
      id: interfaz.inventario_paquetes
      nombre: inventario_paquetes
      tipo: capacidad
      modulo: interfaz
    [222]
      id: interfaz.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: interfaz
    [223]
      id: interfaz.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: interfaz
    [224]
      id: interfaz.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: interfaz
    [225]
      id: interfaz.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: interfaz
    [226]
      id: RE
      nombre: realidad
      rol: RE
      tipo: modulo
    [227]
      id: realidad.verificar
      nombre: verificar
      tipo: capacidad
      modulo: realidad
    [228]
      id: realidad.barrer
      nombre: barrer
      tipo: capacidad
      modulo: realidad
    [229]
      id: realidad.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: realidad
    [230]
      id: realidad.inventario
      nombre: inventario
      tipo: capacidad
      modulo: realidad
    [231]
      id: realidad.reporte
      nombre: reporte
      tipo: capacidad
      modulo: realidad
    [232]
      id: realidad.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: realidad
    [233]
      id: realidad.registrar_resultado_dominio
      nombre: registrar_resultado_dominio
      tipo: capacidad
      modulo: realidad
    [234]
      id: realidad.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: realidad
    [235]
      id: realidad.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: realidad
    [236]
      id: realidad.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: realidad
    [237]
      id: realidad.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: realidad
    [238]
      id: SF
      nombre: self
      rol: SF
      tipo: modulo
    [239]
      id: self.verificar
      nombre: verificar
      tipo: capacidad
      modulo: self
    [240]
      id: self.barrer
      nombre: barrer
      tipo: capacidad
      modulo: self
    [241]
      id: self.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: self
    [242]
      id: self.yo_funcional
      nombre: yo_funcional
      tipo: capacidad
      modulo: self
    [243]
      id: self.oscilar
      nombre: oscilar
      tipo: capacidad
      modulo: self
    [244]
      id: self.desde_donde
      nombre: desde_donde
      tipo: capacidad
      modulo: self
    [245]
      id: self.estado_self
      nombre: estado_self
      tipo: capacidad
      modulo: self
    [246]
      id: self.elegir
      nombre: elegir
      tipo: capacidad
      modulo: self
    [247]
      id: self.inventario
      nombre: inventario
      tipo: capacidad
      modulo: self
    [248]
      id: self.reporte
      nombre: reporte
      tipo: capacidad
      modulo: self
    [249]
      id: self.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: self
    [250]
      id: self.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: self
    [251]
      id: self.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: self
    [252]
      id: self.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: self
    [253]
      id: self.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: self
    [254]
      id: SC
      nombre: spartaco_seguridad
      rol: SC
      tipo: modulo
    [255]
      id: spartaco_seguridad.verificar
      nombre: verificar
      tipo: capacidad
      modulo: spartaco_seguridad
    [256]
      id: spartaco_seguridad.barrer
      nombre: barrer
      tipo: capacidad
      modulo: spartaco_seguridad
    [257]
      id: spartaco_seguridad.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: spartaco_seguridad
    [258]
      id: spartaco_seguridad.inventario
      nombre: inventario
      tipo: capacidad
      modulo: spartaco_seguridad
    [259]
      id: spartaco_seguridad.reporte
      nombre: reporte
      tipo: capacidad
      modulo: spartaco_seguridad
    [260]
      id: spartaco_seguridad.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: spartaco_seguridad
    [261]
      id: spartaco_seguridad.catalogo
      nombre: catalogo
      tipo: capacidad
      modulo: spartaco_seguridad
    [262]
      id: spartaco_seguridad.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: spartaco_seguridad
    [263]
      id: spartaco_seguridad.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: spartaco_seguridad
    [264]
      id: spartaco_seguridad.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: spartaco_seguridad
    [265]
      id: spartaco_seguridad.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: spartaco_seguridad
    [266]
      id: TX
      nombre: taxonomia
      rol: TX
      tipo: modulo
    [267]
      id: taxonomia.verificar
      nombre: verificar
      tipo: capacidad
      modulo: taxonomia
    [268]
      id: taxonomia.barrer
      nombre: barrer
      tipo: capacidad
      modulo: taxonomia
    [269]
      id: taxonomia.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: taxonomia
    [270]
      id: taxonomia.aplicar
      nombre: aplicar
      tipo: capacidad
      modulo: taxonomia
    [271]
      id: taxonomia.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: taxonomia
    [272]
      id: taxonomia.inventario
      nombre: inventario
      tipo: capacidad
      modulo: taxonomia
    [273]
      id: taxonomia.reporte
      nombre: reporte
      tipo: capacidad
      modulo: taxonomia
    [274]
      id: taxonomia.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: taxonomia
    [275]
      id: taxonomia.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: taxonomia
    [276]
      id: taxonomia.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: taxonomia
    [277]
      id: taxonomia.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: taxonomia
    [278]
      id: taxonomia.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: taxonomia
    [279]
      id: TT
      nombre: tru_totales
      rol: TT
      tipo: modulo
    [280]
      id: tru_totales.verificar
      nombre: verificar
      tipo: capacidad
      modulo: tru_totales
    [281]
      id: tru_totales.barrer
      nombre: barrer
      tipo: capacidad
      modulo: tru_totales
    [282]
      id: tru_totales.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: tru_totales
    [283]
      id: tru_totales.categorias
      nombre: categorias
      tipo: capacidad
      modulo: tru_totales
    [284]
      id: tru_totales.capacidades
      nombre: capacidades
      tipo: capacidad
      modulo: tru_totales
    [285]
      id: tru_totales.resolver_pedido
      nombre: resolver_pedido
      tipo: capacidad
      modulo: tru_totales
    [286]
      id: tru_totales.inventario
      nombre: inventario
      tipo: capacidad
      modulo: tru_totales
    [287]
      id: tru_totales.reporte
      nombre: reporte
      tipo: capacidad
      modulo: tru_totales
    [288]
      id: tru_totales.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: tru_totales
    [289]
      id: tru_totales.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: tru_totales
    [290]
      id: tru_totales.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: tru_totales
    [291]
      id: tru_totales.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: tru_totales
    [292]
      id: tru_totales.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: tru_totales
    [293]
      id: VX
      nombre: verificacion
      rol: VX
      tipo: modulo
    [294]
      id: verificacion.verificar
      nombre: verificar
      tipo: capacidad
      modulo: verificacion
    [295]
      id: verificacion.barrer
      nombre: barrer
      tipo: capacidad
      modulo: verificacion
    [296]
      id: verificacion.verificar_salida
      nombre: verificar_salida
      tipo: capacidad
      modulo: verificacion
    [297]
      id: verificacion.axiomas
      nombre: axiomas
      tipo: capacidad
      modulo: verificacion
    [298]
      id: verificacion.inventario
      nombre: inventario
      tipo: capacidad
      modulo: verificacion
    [299]
      id: verificacion.reporte
      nombre: reporte
      tipo: capacidad
      modulo: verificacion
    [300]
      id: verificacion.diagnostico
      nombre: diagnostico
      tipo: capacidad
      modulo: verificacion
    [301]
      id: verificacion.ejecutar_total
      nombre: ejecutar_total
      tipo: capacidad
      modulo: verificacion
    [302]
      id: verificacion.inspeccionar
      nombre: inspeccionar
      tipo: capacidad
      modulo: verificacion
    [303]
      id: verificacion.registrar_inventario
      nombre: registrar_inventario
      tipo: capacidad
      modulo: verificacion
    [304]
      id: verificacion.evaluar_universal
      nombre: evaluar_universal
      tipo: capacidad
      modulo: verificacion
  aristas:
    [0]
      from: axiomas
      to: CE
      tipo: requiere
    [1]
      from: axiomas
      to: AX
      tipo: requiere
    [2]
      from: axiomas
      to: FO
      tipo: requiere
    [3]
      from: axiomas
      to: MC
      tipo: requiere
    [4]
      from: axiomas
      to: SF
      tipo: requiere
    [5]
      from: axiomas
      to: CA
      tipo: requiere
    [6]
      from: axiomas
      to: CX
      tipo: requiere
    [7]
      from: axiomas
      to: DI
      tipo: requiere
    [8]
      from: axiomas
      to: RE
      tipo: requiere
    [9]
      from: axiomas
      to: VX
      tipo: requiere
    [10]
      from: axiomas
      to: TX
      tipo: requiere
    [11]
      from: axiomas
      to: CH
      tipo: requiere
    [12]
      from: axiomas
      to: CIT
      tipo: requiere
    [13]
      from: axiomas
      to: DGCO
      tipo: requiere
    [14]
      from: axiomas
      to: UI
      tipo: requiere
    [15]
      from: axiomas
      to: CC
      tipo: requiere
    [16]
      from: axiomas
      to: TT
      tipo: requiere
    [17]
      from: axiomas
      to: SC
      tipo: requiere
    [18]
      from: axiomas
      to: axiomas.verificar
      tipo: declara_capacidad
    [19]
      from: axiomas
      to: axiomas.barrer
      tipo: declara_capacidad
    [20]
      from: axiomas
      to: axiomas.verificar_salida
      tipo: declara_capacidad
    [21]
      from: axiomas
      to: axiomas.inventario
      tipo: declara_capacidad
    [22]
      from: axiomas
      to: axiomas.axiomas
      tipo: declara_capacidad
    [23]
      from: axiomas
      to: axiomas.declaraciones
      tipo: declara_capacidad
    [24]
      from: axiomas
      to: axiomas.generatividad
      tipo: declara_capacidad
    [25]
      from: axiomas
      to: axiomas.por_dominio
      tipo: declara_capacidad
    [26]
      from: axiomas
      to: axiomas.ids_dominio_k_o
      tipo: declara_capacidad
    [27]
      from: axiomas
      to: axiomas.recolectar
      tipo: declara_capacidad
    [28]
      from: axiomas
      to: axiomas.reporte
      tipo: declara_capacidad
    [29]
      from: axiomas
      to: axiomas.diagnostico
      tipo: declara_capacidad
    [30]
      from: axiomas
      to: axiomas.buscar_por_id
      tipo: declara_capacidad
    [31]
      from: axiomas
      to: axiomas.limite_axiomático
      tipo: declara_capacidad
    [32]
      from: axiomas
      to: axiomas.ejecutar_total
      tipo: declara_capacidad
    [33]
      from: axiomas
      to: axiomas.inspeccionar
      tipo: declara_capacidad
    [34]
      from: axiomas
      to: axiomas.evaluar_universal
      tipo: declara_capacidad
    [35]
      from: cache
      to: CE
      tipo: requiere
    [36]
      from: cache
      to: AX
      tipo: requiere
    [37]
      from: cache
      to: FO
      tipo: requiere
    [38]
      from: cache
      to: MC
      tipo: requiere
    [39]
      from: cache
      to: SF
      tipo: requiere
    [40]
      from: cache
      to: CA
      tipo: requiere
    [41]
      from: cache
      to: CX
      tipo: requiere
    [42]
      from: cache
      to: DI
      tipo: requiere
    [43]
      from: cache
      to: RE
      tipo: requiere
    [44]
      from: cache
      to: VX
      tipo: requiere
    [45]
      from: cache
      to: TX
      tipo: requiere
    [46]
      from: cache
      to: CIT
      tipo: requiere
    [47]
      from: cache
      to: DGCO
      tipo: requiere
    [48]
      from: cache
      to: UI
      tipo: requiere
    [49]
      from: cache
      to: CC
      tipo: requiere
    [50]
      from: cache
      to: TT
      tipo: requiere
    [51]
      from: cache
      to: SC
      tipo: requiere
    [52]
      from: cache
      to: CT
      tipo: requiere
    [53]
      from: cache
      to: cache.verificar
      tipo: declara_capacidad
    [54]
      from: cache
      to: cache.barrer
      tipo: declara_capacidad
    [55]
      from: cache
      to: cache.depositar
      tipo: declara_capacidad
    [56]
      from: cache
      to: cache.leer
      tipo: declara_capacidad
    [57]
      from: cache
      to: cache.leer_eventos
      tipo: declara_capacidad
    [58]
      from: cache
      to: cache.leer_por_ciclo
      tipo: declara_capacidad
    [59]
      from: cache
      to: cache.leer_por_modulo
      tipo: declara_capacidad
    [60]
      from: cache
      to: cache.leer_por_tipo
      tipo: declara_capacidad
    [61]
      from: cache
      to: cache.leer_por_categoria
      tipo: declara_capacidad
    [62]
      from: cache
      to: cache.leer_por_capacidad
      tipo: declara_capacidad
    [63]
      from: cache
      to: cache.leer_por_origen
      tipo: declara_capacidad
    [64]
      from: cache
      to: cache.leer_por_destino
      tipo: declara_capacidad
    [65]
      from: cache
      to: cache.leer_por_estado
      tipo: declara_capacidad
    [66]
      from: cache
      to: cache.leer_por_seq
      tipo: declara_capacidad
    [67]
      from: cache
      to: cache.leer_por_timestamp
      tipo: declara_capacidad
    [68]
      from: cache
      to: cache.categorias
      tipo: declara_capacidad
    [69]
      from: cache
      to: cache.inventario
      tipo: declara_capacidad
    [70]
      from: cache
      to: cache.reporte
      tipo: declara_capacidad
    [71]
      from: cache
      to: cache.diagnostico
      tipo: declara_capacidad
    [72]
      from: cache
      to: cache.verificar_salida
      tipo: declara_capacidad
    [73]
      from: cache
      to: cache.backend_para_centinela
      tipo: declara_capacidad
    [74]
      from: cache
      to: cache.ejecutar_total
      tipo: declara_capacidad
    [75]
      from: cache
      to: cache.inspeccionar
      tipo: declara_capacidad
    [76]
      from: cache
      to: cache.registrar_inventario
      tipo: declara_capacidad
    [77]
      from: cache
      to: cache.mapear_codigo
      tipo: declara_capacidad
    [78]
      from: cache
      to: cache.clasificar_ids
      tipo: declara_capacidad
    [79]
      from: cache
      to: cache.evaluar_universal
      tipo: declara_capacidad
    [80]
      from: calculator
      to: CT
      tipo: requiere
    [81]
      from: calculator
      to: AX
      tipo: requiere
    [82]
      from: calculator
      to: FO
      tipo: requiere
    [83]
      from: calculator
      to: MC
      tipo: requiere
    [84]
      from: calculator
      to: SF
      tipo: requiere
    [85]
      from: calculator
      to: CA
      tipo: requiere
    [86]
      from: calculator
      to: CX
      tipo: requiere
    [87]
      from: calculator
      to: DI
      tipo: requiere
    [88]
      from: calculator
      to: RE
      tipo: requiere
    [89]
      from: calculator
      to: VX
      tipo: requiere
    [90]
      from: calculator
      to: TX
      tipo: requiere
    [91]
      from: calculator
      to: CH
      tipo: requiere
    [92]
      from: calculator
      to: CIT
      tipo: requiere
    [93]
      from: calculator
      to: DGCO
      tipo: requiere
    [94]
      from: calculator
      to: UI
      tipo: requiere
    [95]
      from: calculator
      to: CC
      tipo: requiere
    [96]
      from: calculator
      to: TT
      tipo: requiere
    [97]
      from: calculator
      to: SC
      tipo: requiere
    [98]
      from: calculator
      to: calculator.calcular
      tipo: declara_capacidad
    [99]
      from: calculator
      to: calculator.calcular_C
      tipo: declara_capacidad
    [100]
      from: calculator
      to: calculator.calcular_L
      tipo: declara_capacidad
    [101]
      from: calculator
      to: calculator.calcular_K
      tipo: declara_capacidad
    [102]
      from: calculator
      to: calculator.calcular_factor
      tipo: declara_capacidad
    [103]
      from: calculator
      to: calculator.representar
      tipo: declara_capacidad
    [104]
      from: calculator
      to: calculator.validar_evidencia
      tipo: declara_capacidad
    [105]
      from: calculator
      to: calculator.explicar_calculo
      tipo: declara_capacidad
    [106]
      from: calculator
      to: calculator.verificar
      tipo: declara_capacidad
    [107]
      from: calculator
      to: calculator.barrer
      tipo: declara_capacidad
    [108]
      from: calculator
      to: calculator.inventario
      tipo: declara_capacidad
    [109]
      from: calculator
      to: calculator.reporte
      tipo: declara_capacidad
    [110]
      from: calculator
      to: calculator.diagnostico
      tipo: declara_capacidad
    [111]
      from: calculator
      to: calculator.leer_ids_escala
      tipo: declara_capacidad
    [112]
      from: calculator
      to: calculator.verificar_salida
      tipo: declara_capacidad
    [113]
      from: calculator
      to: calculator.historial
      tipo: declara_capacidad
    [114]
      from: calculator
      to: calculator.verificar_calculo_de_C_L_K
      tipo: declara_capacidad
    [115]
      from: calculator
      to: calculator.ejecutar_total
      tipo: declara_capacidad
    [116]
      from: calculator
      to: calculator.inspeccionar
      tipo: declara_capacidad
    [117]
      from: calculator
      to: calculator.registrar_inventario
      tipo: declara_capacidad
    [118]
      from: calculator
      to: calculator.evaluar_universal
      tipo: declara_capacidad
    [119]
      from: capacidades_engine
      to: AX
      tipo: requiere
    [120]
      from: capacidades_engine
      to: FO
      tipo: requiere
    [121]
      from: capacidades_engine
      to: MC
      tipo: requiere
    [122]
      from: capacidades_engine
      to: SF
      tipo: requiere
    [123]
      from: capacidades_engine
      to: CA
      tipo: requiere
    [124]
      from: capacidades_engine
      to: CX
      tipo: requiere
    [125]
      from: capacidades_engine
      to: DI
      tipo: requiere
    [126]
      from: capacidades_engine
      to: RE
      tipo: requiere
    [127]
      from: capacidades_engine
      to: VX
      tipo: requiere
    [128]
      from: capacidades_engine
      to: TX
      tipo: requiere
    [129]
      from: capacidades_engine
      to: CH
      tipo: requiere
    [130]
      from: capacidades_engine
      to: CIT
      tipo: requiere
    [131]
      from: capacidades_engine
      to: DGCO
      tipo: requiere
    [132]
      from: capacidades_engine
      to: UI
      tipo: requiere
    [133]
      from: capacidades_engine
      to: CC
      tipo: requiere
    [134]
      from: capacidades_engine
      to: TT
      tipo: requiere
    [135]
      from: capacidades_engine
      to: SC
      tipo: requiere
    [136]
      from: capacidades_engine
      to: capacidades_engine.verificar
      tipo: declara_capacidad
    [137]
      from: capacidades_engine
      to: capacidades_engine.barrer
      tipo: declara_capacidad
    [138]
      from: capacidades_engine
      to: capacidades_engine.inventario
      tipo: declara_capacidad
    [139]
      from: capacidades_engine
      to: capacidades_engine.skills
      tipo: declara_capacidad
    [140]
      from: capacidades_engine
      to: capacidades_engine.ids
      tipo: declara_capacidad
    [141]
      from: capacidades_engine
      to: capacidades_engine.por_id
      tipo: declara_capacidad
    [142]
      from: capacidades_engine
      to: capacidades_engine.listar_archivos
      tipo: declara_capacidad
    [143]
      from: capacidades_engine
      to: capacidades_engine.verificar_salida
      tipo: declara_capacidad
    [144]
      from: capacidades_engine
      to: capacidades_engine.ejecutar_total
      tipo: declara_capacidad
    [145]
      from: capacidades_engine
      to: capacidades_engine.inspeccionar
      tipo: declara_capacidad
    [146]
      from: capacidades_engine
      to: capacidades_engine.registrar_inventario
      tipo: declara_capacidad
    [147]
      from: capacidades_engine
      to: capacidades_engine.reporte
      tipo: declara_capacidad
    [148]
      from: capacidades_engine
      to: capacidades_engine.diagnostico
      tipo: declara_capacidad
    [149]
      from: capacidades_engine
      to: capacidades_engine.evaluar_universal
      tipo: declara_capacidad
    [150]
      from: catalogo_citaciones
      to: CE
      tipo: requiere
    [151]
      from: catalogo_citaciones
      to: AX
      tipo: requiere
    [152]
      from: catalogo_citaciones
      to: FO
      tipo: requiere
    [153]
      from: catalogo_citaciones
      to: MC
      tipo: requiere
    [154]
      from: catalogo_citaciones
      to: SF
      tipo: requiere
    [155]
      from: catalogo_citaciones
      to: CA
      tipo: requiere
    [156]
      from: catalogo_citaciones
      to: CX
      tipo: requiere
    [157]
      from: catalogo_citaciones
      to: DI
      tipo: requiere
    [158]
      from: catalogo_citaciones
      to: RE
      tipo: requiere
    [159]
      from: catalogo_citaciones
      to: VX
      tipo: requiere
    [160]
      from: catalogo_citaciones
      to: TX
      tipo: requiere
    [161]
      from: catalogo_citaciones
      to: CH
      tipo: requiere
    [162]
      from: catalogo_citaciones
      to: CIT
      tipo: requiere
    [163]
      from: catalogo_citaciones
      to: DGCO
      tipo: requiere
    [164]
      from: catalogo_citaciones
      to: UI
      tipo: requiere
    [165]
      from: catalogo_citaciones
      to: TT
      tipo: requiere
    [166]
      from: catalogo_citaciones
      to: SC
      tipo: requiere
    [167]
      from: catalogo_citaciones
      to: catalogo_citaciones.verificar
      tipo: declara_capacidad
    [168]
      from: catalogo_citaciones
      to: catalogo_citaciones.barrer
      tipo: declara_capacidad
    [169]
      from: catalogo_citaciones
      to: catalogo_citaciones.inventario
      tipo: declara_capacidad
    [170]
      from: catalogo_citaciones
      to: catalogo_citaciones.categorias
      tipo: declara_capacidad
    [171]
      from: catalogo_citaciones
      to: catalogo_citaciones.por_id
      tipo: declara_capacidad
    [172]
      from: catalogo_citaciones
      to: catalogo_citaciones.ids
      tipo: declara_capacidad
    [173]
      from: catalogo_citaciones
      to: catalogo_citaciones.esquema
      tipo: declara_capacidad
    [174]
      from: catalogo_citaciones
      to: catalogo_citaciones.reporte
      tipo: declara_capacidad
    [175]
      from: catalogo_citaciones
      to: catalogo_citaciones.diagnostico
      tipo: declara_capacidad
    [176]
      from: catalogo_citaciones
      to: catalogo_citaciones.verificar_salida
      tipo: declara_capacidad
    [177]
      from: catalogo_citaciones
      to: catalogo_citaciones.ejecutar_total
      tipo: declara_capacidad
    [178]
      from: catalogo_citaciones
      to: catalogo_citaciones.inspeccionar
      tipo: declara_capacidad
    [179]
      from: catalogo_citaciones
      to: catalogo_citaciones.registrar_inventario
      tipo: declara_capacidad
    [180]
      from: catalogo_citaciones
      to: catalogo_citaciones.evaluar_universal
      tipo: declara_capacidad
    [181]
      from: citacion
      to: CE
      tipo: requiere
    [182]
      from: citacion
      to: AX
      tipo: requiere
    [183]
      from: citacion
      to: FO
      tipo: requiere
    [184]
      from: citacion
      to: MC
      tipo: requiere
    [185]
      from: citacion
      to: SF
      tipo: requiere
    [186]
      from: citacion
      to: CA
      tipo: requiere
    [187]
      from: citacion
      to: CX
      tipo: requiere
    [188]
      from: citacion
      to: DI
      tipo: requiere
    [189]
      from: citacion
      to: RE
      tipo: requiere
    [190]
      from: citacion
      to: VX
      tipo: requiere
    [191]
      from: citacion
      to: TX
      tipo: requiere
    [192]
      from: citacion
      to: CH
      tipo: requiere
    [193]
      from: citacion
      to: CIT
      tipo: requiere
    [194]
      from: citacion
      to: DGCO
      tipo: requiere
    [195]
      from: citacion
      to: UI
      tipo: requiere
    [196]
      from: citacion
      to: CC
      tipo: requiere
    [197]
      from: citacion
      to: TT
      tipo: requiere
    [198]
      from: citacion
      to: SC
      tipo: requiere
    [199]
      from: citacion
      to: CT
      tipo: requiere
    [200]
      from: citacion
      to: citacion.verificar
      tipo: declara_capacidad
    [201]
      from: citacion
      to: citacion.barrer
      tipo: declara_capacidad
    [202]
      from: citacion
      to: citacion.verificar_salida
      tipo: declara_capacidad
    [203]
      from: citacion
      to: citacion.inventario
      tipo: declara_capacidad
    [204]
      from: citacion
      to: citacion.reporte
      tipo: declara_capacidad
    [205]
      from: citacion
      to: citacion.diagnostico
      tipo: declara_capacidad
    [206]
      from: citacion
      to: citacion.anunciar
      tipo: declara_capacidad
    [207]
      from: citacion
      to: citacion.anunciar_todo
      tipo: declara_capacidad
    [208]
      from: citacion
      to: citacion.citar
      tipo: declara_capacidad
    [209]
      from: citacion
      to: citacion.registrar
      tipo: declara_capacidad
    [210]
      from: citacion
      to: citacion.resolver
      tipo: declara_capacidad
    [211]
      from: citacion
      to: citacion.resolver_enunciado
      tipo: declara_capacidad
    [212]
      from: citacion
      to: citacion.buscar
      tipo: declara_capacidad
    [213]
      from: citacion
      to: citacion.cadena
      tipo: declara_capacidad
    [214]
      from: citacion
      to: citacion.explicar
      tipo: declara_capacidad
    [215]
      from: citacion
      to: citacion.relacionar
      tipo: declara_capacidad
    [216]
      from: citacion
      to: citacion.limpiar_ciclo
      tipo: declara_capacidad
    [217]
      from: citacion
      to: citacion.evaluar
      tipo: declara_capacidad
    [218]
      from: citacion
      to: citacion.ejecutar_total
      tipo: declara_capacidad
    [219]
      from: citacion
      to: citacion.inspeccionar
      tipo: declara_capacidad
    [220]
      from: citacion
      to: citacion.registrar_inventario
      tipo: declara_capacidad
    [221]
      from: citacion
      to: citacion.evaluar_universal
      tipo: declara_capacidad
    [222]
      from: constante
      to: CE
      tipo: requiere
    [223]
      from: constante
      to: AX
      tipo: requiere
    [224]
      from: constante
      to: FO
      tipo: requiere
    [225]
      from: constante
      to: MC
      tipo: requiere
    [226]
      from: constante
      to: SF
      tipo: requiere
    [227]
      from: constante
      to: CA
      tipo: requiere
    [228]
      from: constante
      to: CX
      tipo: requiere
    [229]
      from: constante
      to: DI
      tipo: requiere
    [230]
      from: constante
      to: RE
      tipo: requiere
    [231]
      from: constante
      to: VX
      tipo: requiere
    [232]
      from: constante
      to: TX
      tipo: requiere
    [233]
      from: constante
      to: CH
      tipo: requiere
    [234]
      from: constante
      to: CIT
      tipo: requiere
    [235]
      from: constante
      to: DGCO
      tipo: requiere
    [236]
      from: constante
      to: UI
      tipo: requiere
    [237]
      from: constante
      to: CC
      tipo: requiere
    [238]
      from: constante
      to: TT
      tipo: requiere
    [239]
      from: constante
      to: SC
      tipo: requiere
    [240]
      from: constante
      to: constante.alpha
      tipo: declara_capacidad
    [241]
      from: constante
      to: constante.beta
      tipo: declara_capacidad
    [242]
      from: constante
      to: constante.buscar_constante
      tipo: declara_capacidad
    [243]
      from: constante
      to: constante.descubrir_constantes
      tipo: declara_capacidad
    [244]
      from: constante
      to: constante.diagnostico
      tipo: declara_capacidad
    [245]
      from: constante
      to: constante.ejecutar_total
      tipo: declara_capacidad
    [246]
      from: constante
      to: constante.evaluar_universal
      tipo: declara_capacidad
    [247]
      from: constante
      to: constante.inspeccionar
      tipo: declara_capacidad
    [248]
      from: constante
      to: constante.inventario
      tipo: declara_capacidad
    [249]
      from: constante
      to: constante.listar_constantes
      tipo: declara_capacidad
    [250]
      from: constante
      to: constante.registrar_inventario
      tipo: declara_capacidad
    [251]
      from: constante
      to: constante.reporte
      tipo: declara_capacidad
    [252]
      from: constante
      to: constante.verificar
      tipo: declara_capacidad
    [253]
      from: constante
      to: constante.verificar_constantes
      tipo: declara_capacidad
    [254]
      from: contexto
      to: CE
      tipo: requiere
    [255]
      from: contexto
      to: AX
      tipo: requiere
    [256]
      from: contexto
      to: FO
      tipo: requiere
    [257]
      from: contexto
      to: MC
      tipo: requiere
    [258]
      from: contexto
      to: SF
      tipo: requiere
    [259]
      from: contexto
      to: CA
      tipo: requiere
    [260]
      from: contexto
      to: DI
      tipo: requiere
    [261]
      from: contexto
      to: RE
      tipo: requiere
    [262]
      from: contexto
      to: VX
      tipo: requiere
    [263]
      from: contexto
      to: TX
      tipo: requiere
    [264]
      from: contexto
      to: CH
      tipo: requiere
    [265]
      from: contexto
      to: CIT
      tipo: requiere
    [266]
      from: contexto
      to: DGCO
      tipo: requiere
    [267]
      from: contexto
      to: UI
      tipo: requiere
    [268]
      from: contexto
      to: CC
      tipo: requiere
    [269]
      from: contexto
      to: TT
      tipo: requiere
    [270]
      from: contexto
      to: SC
      tipo: requiere
    [271]
      from: contexto
      to: CT
      tipo: requiere
    [272]
      from: contexto
      to: contexto.resolver
      tipo: declara_capacidad
    [273]
      from: contexto
      to: contexto.evaluar
      tipo: declara_capacidad
    [274]
      from: contexto
      to: contexto.centinela
      tipo: declara_capacidad
    [275]
      from: contexto
      to: contexto.verificar
      tipo: declara_capacidad
    [276]
      from: contexto
      to: contexto.barrer
      tipo: declara_capacidad
    [277]
      from: contexto
      to: contexto.inventario
      tipo: declara_capacidad
    [278]
      from: contexto
      to: contexto.reporte
      tipo: declara_capacidad
    [279]
      from: contexto
      to: contexto.diagnostico
      tipo: declara_capacidad
    [280]
      from: contexto
      to: contexto.axiomas
      tipo: declara_capacidad
    [281]
      from: contexto
      to: contexto.verificar_salida
      tipo: declara_capacidad
    [282]
      from: contexto
      to: contexto.ejecutar
      tipo: declara_capacidad
    [283]
      from: contexto
      to: contexto.ejecutar_total
      tipo: declara_capacidad
    [284]
      from: contexto
      to: contexto.registrar_inventario
      tipo: declara_capacidad
    [285]
      from: contexto
      to: contexto.evaluar_universal
      tipo: declara_capacidad
    [286]
      from: correlacion_mecanica
      to: CE
      tipo: requiere
    [287]
      from: correlacion_mecanica
      to: AX
      tipo: requiere
    [288]
      from: correlacion_mecanica
      to: FO
      tipo: requiere
    [289]
      from: correlacion_mecanica
      to: SF
      tipo: requiere
    [290]
      from: correlacion_mecanica
      to: CA
      tipo: requiere
    [291]
      from: correlacion_mecanica
      to: CX
      tipo: requiere
    [292]
      from: correlacion_mecanica
      to: DI
      tipo: requiere
    [293]
      from: correlacion_mecanica
      to: RE
      tipo: requiere
    [294]
      from: correlacion_mecanica
      to: VX
      tipo: requiere
    [295]
      from: correlacion_mecanica
      to: TX
      tipo: requiere
    [296]
      from: correlacion_mecanica
      to: CH
      tipo: requiere
    [297]
      from: correlacion_mecanica
      to: CIT
      tipo: requiere
    [298]
      from: correlacion_mecanica
      to: DGCO
      tipo: requiere
    [299]
      from: correlacion_mecanica
      to: UI
      tipo: requiere
    [300]
      from: correlacion_mecanica
      to: CC
      tipo: requiere
    [301]
      from: correlacion_mecanica
      to: TT
      tipo: requiere
    [302]
      from: correlacion_mecanica
      to: SC
      tipo: requiere
    [303]
      from: correlacion_mecanica
      to: CT
      tipo: requiere
    [304]
      from: correlacion_mecanica
      to: correlacion_mecanica.axiomas
      tipo: declara_capacidad
    [305]
      from: correlacion_mecanica
      to: correlacion_mecanica.barrer
      tipo: declara_capacidad
    [306]
      from: correlacion_mecanica
      to: correlacion_mecanica.diagnostico
      tipo: declara_capacidad
    [307]
      from: correlacion_mecanica
      to: correlacion_mecanica.ejecutar_total
      tipo: declara_capacidad
    [308]
      from: correlacion_mecanica
      to: correlacion_mecanica.evaluar
      tipo: declara_capacidad
    [309]
      from: correlacion_mecanica
      to: correlacion_mecanica.evaluar_universal
      tipo: declara_capacidad
    [310]
      from: correlacion_mecanica
      to: correlacion_mecanica.inspeccionar
      tipo: declara_capacidad
    [311]
      from: correlacion_mecanica
      to: correlacion_mecanica.inventario
      tipo: declara_capacidad
    [312]
      from: correlacion_mecanica
      to: correlacion_mecanica.listar_mecanicas
      tipo: declara_capacidad
    [313]
      from: correlacion_mecanica
      to: correlacion_mecanica.registrar_inventario
      tipo: declara_capacidad
    [314]
      from: correlacion_mecanica
      to: correlacion_mecanica.reporte
      tipo: declara_capacidad
    [315]
      from: correlacion_mecanica
      to: correlacion_mecanica.verificar
      tipo: declara_capacidad
    [316]
      from: correlacion_mecanica
      to: correlacion_mecanica.verificar_salida
      tipo: declara_capacidad
    [317]
      from: diagnosticoD
      to: *
      tipo: requiere
    [318]
      from: diagnosticoD
      to: diagnosticoD.censo
      tipo: declara_capacidad
    [319]
      from: diagnosticoD
      to: diagnosticoD.verificar
      tipo: declara_capacidad
    [320]
      from: diagnosticoD
      to: diagnosticoD.barrer
      tipo: declara_capacidad
    [321]
      from: diagnosticoD
      to: diagnosticoD.presentar
      tipo: declara_capacidad
    [322]
      from: diagnosticoD
      to: diagnosticoD.reportar
      tipo: declara_capacidad
    [323]
      from: diagnosticoD
      to: diagnosticoD.inventario
      tipo: declara_capacidad
    [324]
      from: diagnosticoD
      to: diagnosticoD.reporte
      tipo: declara_capacidad
    [325]
      from: diagnosticoD
      to: diagnosticoD.diagnostico
      tipo: declara_capacidad
    [326]
      from: diagnosticoD
      to: diagnosticoD.ejecutar_total
      tipo: declara_capacidad
    [327]
      from: diagnosticoD
      to: diagnosticoD.inspeccionar
      tipo: declara_capacidad
    [328]
      from: diagnosticoD
      to: diagnosticoD.registrar_inventario
      tipo: declara_capacidad
    [329]
      from: diagnosticoD
      to: diagnosticoD.evaluar_universal
      tipo: declara_capacidad
    [330]
      from: diccionario
      to: CE
      tipo: requiere
    [331]
      from: diccionario
      to: AX
      tipo: requiere
    [332]
      from: diccionario
      to: FO
      tipo: requiere
    [333]
      from: diccionario
      to: MC
      tipo: requiere
    [334]
      from: diccionario
      to: SF
      tipo: requiere
    [335]
      from: diccionario
      to: CA
      tipo: requiere
    [336]
      from: diccionario
      to: CX
      tipo: requiere
    [337]
      from: diccionario
      to: RE
      tipo: requiere
    [338]
      from: diccionario
      to: VX
      tipo: requiere
    [339]
      from: diccionario
      to: TX
      tipo: requiere
    [340]
      from: diccionario
      to: CH
      tipo: requiere
    [341]
      from: diccionario
      to: CIT
      tipo: requiere
    [342]
      from: diccionario
      to: DGCO
      tipo: requiere
    [343]
      from: diccionario
      to: UI
      tipo: requiere
    [344]
      from: diccionario
      to: CC
      tipo: requiere
    [345]
      from: diccionario
      to: TT
      tipo: requiere
    [346]
      from: diccionario
      to: SC
      tipo: requiere
    [347]
      from: diccionario
      to: CT
      tipo: requiere
    [348]
      from: diccionario
      to: diccionario.verificar
      tipo: declara_capacidad
    [349]
      from: diccionario
      to: diccionario.barrer
      tipo: declara_capacidad
    [350]
      from: diccionario
      to: diccionario.verificar_salida
      tipo: declara_capacidad
    [351]
      from: diccionario
      to: diccionario.inventario
      tipo: declara_capacidad
    [352]
      from: diccionario
      to: diccionario.reporte
      tipo: declara_capacidad
    [353]
      from: diccionario
      to: diccionario.diagnostico
      tipo: declara_capacidad
    [354]
      from: diccionario
      to: diccionario.axiomas
      tipo: declara_capacidad
    [355]
      from: diccionario
      to: diccionario.resolver
      tipo: declara_capacidad
    [356]
      from: diccionario
      to: diccionario.listar
      tipo: declara_capacidad
    [357]
      from: diccionario
      to: diccionario.cargar
      tipo: declara_capacidad
    [358]
      from: diccionario
      to: diccionario.cargar_todos
      tipo: declara_capacidad
    [359]
      from: diccionario
      to: diccionario.definir
      tipo: declara_capacidad
    [360]
      from: diccionario
      to: diccionario.significado
      tipo: declara_capacidad
    [361]
      from: diccionario
      to: diccionario.palabras
      tipo: declara_capacidad
    [362]
      from: diccionario
      to: diccionario.inyectar_en_peticion
      tipo: declara_capacidad
    [363]
      from: diccionario
      to: diccionario.ejecutar_total
      tipo: declara_capacidad
    [364]
      from: diccionario
      to: diccionario.inspeccionar
      tipo: declara_capacidad
    [365]
      from: diccionario
      to: diccionario.registrar_inventario
      tipo: declara_capacidad
    [366]
      from: diccionario
      to: diccionario.evaluar_universal
      tipo: declara_capacidad
    [367]
      from: formulas
      to: CE
      tipo: requiere
    [368]
      from: formulas
      to: AX
      tipo: requiere
    [369]
      from: formulas
      to: MC
      tipo: requiere
    [370]
      from: formulas
      to: SF
      tipo: requiere
    [371]
      from: formulas
      to: CA
      tipo: requiere
    [372]
      from: formulas
      to: CX
      tipo: requiere
    [373]
      from: formulas
      to: DI
      tipo: requiere
    [374]
      from: formulas
      to: RE
      tipo: requiere
    [375]
      from: formulas
      to: VX
      tipo: requiere
    [376]
      from: formulas
      to: TX
      tipo: requiere
    [377]
      from: formulas
      to: CH
      tipo: requiere
    [378]
      from: formulas
      to: CIT
      tipo: requiere
    [379]
      from: formulas
      to: DGCO
      tipo: requiere
    [380]
      from: formulas
      to: UI
      tipo: requiere
    [381]
      from: formulas
      to: CC
      tipo: requiere
    [382]
      from: formulas
      to: TT
      tipo: requiere
    [383]
      from: formulas
      to: SC
      tipo: requiere
    [384]
      from: formulas
      to: CT
      tipo: requiere
    [385]
      from: formulas
      to: formulas.verificar
      tipo: declara_capacidad
    [386]
      from: formulas
      to: formulas.barrer
      tipo: declara_capacidad
    [387]
      from: formulas
      to: formulas.evaluar
      tipo: declara_capacidad
    [388]
      from: formulas
      to: formulas.verificar_salida
      tipo: declara_capacidad
    [389]
      from: formulas
      to: formulas.inventario
      tipo: declara_capacidad
    [390]
      from: formulas
      to: formulas.axiomas
      tipo: declara_capacidad
    [391]
      from: formulas
      to: formulas.tru_ri
      tipo: declara_capacidad
    [392]
      from: formulas
      to: formulas.tru_total
      tipo: declara_capacidad
    [393]
      from: formulas
      to: formulas.reporte
      tipo: declara_capacidad
    [394]
      from: formulas
      to: formulas.diagnostico
      tipo: declara_capacidad
    [395]
      from: formulas
      to: formulas.listar_formulas
      tipo: declara_capacidad
    [396]
      from: formulas
      to: formulas.ejecutar_total
      tipo: declara_capacidad
    [397]
      from: formulas
      to: formulas.inspeccionar
      tipo: declara_capacidad
    [398]
      from: formulas
      to: formulas.registrar_inventario
      tipo: declara_capacidad
    [399]
      from: formulas
      to: formulas.evaluar_universal
      tipo: declara_capacidad
    [400]
      from: interfaz
      to: CE
      tipo: requiere
    [401]
      from: interfaz
      to: AX
      tipo: requiere
    [402]
      from: interfaz
      to: FO
      tipo: requiere
    [403]
      from: interfaz
      to: MC
      tipo: requiere
    [404]
      from: interfaz
      to: SF
      tipo: requiere
    [405]
      from: interfaz
      to: CA
      tipo: requiere
    [406]
      from: interfaz
      to: CX
      tipo: requiere
    [407]
      from: interfaz
      to: DI
      tipo: requiere
    [408]
      from: interfaz
      to: RE
      tipo: requiere
    [409]
      from: interfaz
      to: VX
      tipo: requiere
    [410]
      from: interfaz
      to: TX
      tipo: requiere
    [411]
      from: interfaz
      to: CH
      tipo: requiere
    [412]
      from: interfaz
      to: CIT
      tipo: requiere
    [413]
      from: interfaz
      to: DGCO
      tipo: requiere
    [414]
      from: interfaz
      to: CC
      tipo: requiere
    [415]
      from: interfaz
      to: TT
      tipo: requiere
    [416]
      from: interfaz
      to: SC
      tipo: requiere
    [417]
      from: interfaz
      to: CT
      tipo: requiere
    [418]
      from: interfaz
      to: interfaz.verificar
      tipo: declara_capacidad
    [419]
      from: interfaz
      to: interfaz.barrer
      tipo: declara_capacidad
    [420]
      from: interfaz
      to: interfaz.componer
      tipo: declara_capacidad
    [421]
      from: interfaz
      to: interfaz.observar
      tipo: declara_capacidad
    [422]
      from: interfaz
      to: interfaz.axiomas
      tipo: declara_capacidad
    [423]
      from: interfaz
      to: interfaz.inventario
      tipo: declara_capacidad
    [424]
      from: interfaz
      to: interfaz.inventario_paquetes
      tipo: declara_capacidad
    [425]
      from: interfaz
      to: interfaz.ejecutar_total
      tipo: declara_capacidad
    [426]
      from: interfaz
      to: interfaz.inspeccionar
      tipo: declara_capacidad
    [427]
      from: interfaz
      to: interfaz.registrar_inventario
      tipo: declara_capacidad
    [428]
      from: interfaz
      to: interfaz.evaluar_universal
      tipo: declara_capacidad
    [429]
      from: realidad
      to: CE
      tipo: requiere
    [430]
      from: realidad
      to: AX
      tipo: requiere
    [431]
      from: realidad
      to: FO
      tipo: requiere
    [432]
      from: realidad
      to: MC
      tipo: requiere
    [433]
      from: realidad
      to: SF
      tipo: requiere
    [434]
      from: realidad
      to: CA
      tipo: requiere
    [435]
      from: realidad
      to: CX
      tipo: requiere
    [436]
      from: realidad
      to: DI
      tipo: requiere
    [437]
      from: realidad
      to: VX
      tipo: requiere
    [438]
      from: realidad
      to: TX
      tipo: requiere
    [439]
      from: realidad
      to: CH
      tipo: requiere
    [440]
      from: realidad
      to: CIT
      tipo: requiere
    [441]
      from: realidad
      to: DGCO
      tipo: requiere
    [442]
      from: realidad
      to: UI
      tipo: requiere
    [443]
      from: realidad
      to: CC
      tipo: requiere
    [444]
      from: realidad
      to: TT
      tipo: requiere
    [445]
      from: realidad
      to: SC
      tipo: requiere
    [446]
      from: realidad
      to: CT
      tipo: requiere
    [447]
      from: realidad
      to: realidad.verificar
      tipo: declara_capacidad
    [448]
      from: realidad
      to: realidad.barrer
      tipo: declara_capacidad
    [449]
      from: realidad
      to: realidad.verificar_salida
      tipo: declara_capacidad
    [450]
      from: realidad
      to: realidad.inventario
      tipo: declara_capacidad
    [451]
      from: realidad
      to: realidad.reporte
      tipo: declara_capacidad
    [452]
      from: realidad
      to: realidad.diagnostico
      tipo: declara_capacidad
    [453]
      from: realidad
      to: realidad.registrar_resultado_dominio
      tipo: declara_capacidad
    [454]
      from: realidad
      to: realidad.ejecutar_total
      tipo: declara_capacidad
    [455]
      from: realidad
      to: realidad.inspeccionar
      tipo: declara_capacidad
    [456]
      from: realidad
      to: realidad.evaluar_universal
      tipo: declara_capacidad
    [457]
      from: realidad
      to: realidad.registrar_inventario
      tipo: declara_capacidad
    [458]
      from: self
      to: CE
      tipo: requiere
    [459]
      from: self
      to: AX
      tipo: requiere
    [460]
      from: self
      to: FO
      tipo: requiere
    [461]
      from: self
      to: MC
      tipo: requiere
    [462]
      from: self
      to: CA
      tipo: requiere
    [463]
      from: self
      to: CX
      tipo: requiere
    [464]
      from: self
      to: DI
      tipo: requiere
    [465]
      from: self
      to: RE
      tipo: requiere
    [466]
      from: self
      to: VX
      tipo: requiere
    [467]
      from: self
      to: TX
      tipo: requiere
    [468]
      from: self
      to: CH
      tipo: requiere
    [469]
      from: self
      to: CIT
      tipo: requiere
    [470]
      from: self
      to: DGCO
      tipo: requiere
    [471]
      from: self
      to: UI
      tipo: requiere
    [472]
      from: self
      to: CC
      tipo: requiere
    [473]
      from: self
      to: TT
      tipo: requiere
    [474]
      from: self
      to: SC
      tipo: requiere
    [475]
      from: self
      to: CT
      tipo: requiere
    [476]
      from: self
      to: self.verificar
      tipo: declara_capacidad
    [477]
      from: self
      to: self.barrer
      tipo: declara_capacidad
    [478]
      from: self
      to: self.verificar_salida
      tipo: declara_capacidad
    [479]
      from: self
      to: self.yo_funcional
      tipo: declara_capacidad
    [480]
      from: self
      to: self.oscilar
      tipo: declara_capacidad
    [481]
      from: self
      to: self.desde_donde
      tipo: declara_capacidad
    [482]
      from: self
      to: self.estado_self
      tipo: declara_capacidad
    [483]
      from: self
      to: self.elegir
      tipo: declara_capacidad
    [484]
      from: self
      to: self.inventario
      tipo: declara_capacidad
    [485]
      from: self
      to: self.reporte
      tipo: declara_capacidad
    [486]
      from: self
      to: self.diagnostico
      tipo: declara_capacidad
    [487]
      from: self
      to: self.ejecutar_total
      tipo: declara_capacidad
    [488]
      from: self
      to: self.inspeccionar
      tipo: declara_capacidad
    [489]
      from: self
      to: self.registrar_inventario
      tipo: declara_capacidad
    [490]
      from: self
      to: self.evaluar_universal
      tipo: declara_capacidad
    [491]
      from: spartaco_seguridad
      to: CE
      tipo: requiere
    [492]
      from: spartaco_seguridad
      to: AX
      tipo: requiere
    [493]
      from: spartaco_seguridad
      to: FO
      tipo: requiere
    [494]
      from: spartaco_seguridad
      to: MC
      tipo: requiere
    [495]
      from: spartaco_seguridad
      to: SF
      tipo: requiere
    [496]
      from: spartaco_seguridad
      to: CA
      tipo: requiere
    [497]
      from: spartaco_seguridad
      to: CX
      tipo: requiere
    [498]
      from: spartaco_seguridad
      to: DI
      tipo: requiere
    [499]
      from: spartaco_seguridad
      to: RE
      tipo: requiere
    [500]
      from: spartaco_seguridad
      to: VX
      tipo: requiere
    [501]
      from: spartaco_seguridad
      to: TX
      tipo: requiere
    [502]
      from: spartaco_seguridad
      to: CH
      tipo: requiere
    [503]
      from: spartaco_seguridad
      to: CIT
      tipo: requiere
    [504]
      from: spartaco_seguridad
      to: DGCO
      tipo: requiere
    [505]
      from: spartaco_seguridad
      to: UI
      tipo: requiere
    [506]
      from: spartaco_seguridad
      to: CC
      tipo: requiere
    [507]
      from: spartaco_seguridad
      to: TT
      tipo: requiere
    [508]
      from: spartaco_seguridad
      to: CT
      tipo: requiere
    [509]
      from: spartaco_seguridad
      to: spartaco_seguridad.verificar
      tipo: declara_capacidad
    [510]
      from: spartaco_seguridad
      to: spartaco_seguridad.barrer
      tipo: declara_capacidad
    [511]
      from: spartaco_seguridad
      to: spartaco_seguridad.verificar_salida
      tipo: declara_capacidad
    [512]
      from: spartaco_seguridad
      to: spartaco_seguridad.inventario
      tipo: declara_capacidad
    [513]
      from: spartaco_seguridad
      to: spartaco_seguridad.reporte
      tipo: declara_capacidad
    [514]
      from: spartaco_seguridad
      to: spartaco_seguridad.diagnostico
      tipo: declara_capacidad
    [515]
      from: spartaco_seguridad
      to: spartaco_seguridad.catalogo
      tipo: declara_capacidad
    [516]
      from: spartaco_seguridad
      to: spartaco_seguridad.ejecutar_total
      tipo: declara_capacidad
    [517]
      from: spartaco_seguridad
      to: spartaco_seguridad.inspeccionar
      tipo: declara_capacidad
    [518]
      from: spartaco_seguridad
      to: spartaco_seguridad.registrar_inventario
      tipo: declara_capacidad
    [519]
      from: spartaco_seguridad
      to: spartaco_seguridad.evaluar_universal
      tipo: declara_capacidad
    [520]
      from: taxonomia
      to: CE
      tipo: requiere
    [521]
      from: taxonomia
      to: AX
      tipo: requiere
    [522]
      from: taxonomia
      to: FO
      tipo: requiere
    [523]
      from: taxonomia
      to: MC
      tipo: requiere
    [524]
      from: taxonomia
      to: SF
      tipo: requiere
    [525]
      from: taxonomia
      to: CA
      tipo: requiere
    [526]
      from: taxonomia
      to: CX
      tipo: requiere
    [527]
      from: taxonomia
      to: DI
      tipo: requiere
    [528]
      from: taxonomia
      to: RE
      tipo: requiere
    [529]
      from: taxonomia
      to: VX
      tipo: requiere
    [530]
      from: taxonomia
      to: CH
      tipo: requiere
    [531]
      from: taxonomia
      to: CIT
      tipo: requiere
    [532]
      from: taxonomia
      to: DGCO
      tipo: requiere
    [533]
      from: taxonomia
      to: UI
      tipo: requiere
    [534]
      from: taxonomia
      to: CC
      tipo: requiere
    [535]
      from: taxonomia
      to: TT
      tipo: requiere
    [536]
      from: taxonomia
      to: SC
      tipo: requiere
    [537]
      from: taxonomia
      to: CT
      tipo: requiere
    [538]
      from: taxonomia
      to: taxonomia.verificar
      tipo: declara_capacidad
    [539]
      from: taxonomia
      to: taxonomia.barrer
      tipo: declara_capacidad
    [540]
      from: taxonomia
      to: taxonomia.verificar_salida
      tipo: declara_capacidad
    [541]
      from: taxonomia
      to: taxonomia.aplicar
      tipo: declara_capacidad
    [542]
      from: taxonomia
      to: taxonomia.axiomas
      tipo: declara_capacidad
    [543]
      from: taxonomia
      to: taxonomia.inventario
      tipo: declara_capacidad
    [544]
      from: taxonomia
      to: taxonomia.reporte
      tipo: declara_capacidad
    [545]
      from: taxonomia
      to: taxonomia.diagnostico
      tipo: declara_capacidad
    [546]
      from: taxonomia
      to: taxonomia.ejecutar_total
      tipo: declara_capacidad
    [547]
      from: taxonomia
      to: taxonomia.inspeccionar
      tipo: declara_capacidad
    [548]
      from: taxonomia
      to: taxonomia.registrar_inventario
      tipo: declara_capacidad
    [549]
      from: taxonomia
      to: taxonomia.evaluar_universal
      tipo: declara_capacidad
    [550]
      from: tru_totales
      to: CE
      tipo: requiere
    [551]
      from: tru_totales
      to: AX
      tipo: requiere
    [552]
      from: tru_totales
      to: FO
      tipo: requiere
    [553]
      from: tru_totales
      to: MC
      tipo: requiere
    [554]
      from: tru_totales
      to: SF
      tipo: requiere
    [555]
      from: tru_totales
      to: CA
      tipo: requiere
    [556]
      from: tru_totales
      to: CX
      tipo: requiere
    [557]
      from: tru_totales
      to: DI
      tipo: requiere
    [558]
      from: tru_totales
      to: RE
      tipo: requiere
    [559]
      from: tru_totales
      to: VX
      tipo: requiere
    [560]
      from: tru_totales
      to: TX
      tipo: requiere
    [561]
      from: tru_totales
      to: CH
      tipo: requiere
    [562]
      from: tru_totales
      to: CIT
      tipo: requiere
    [563]
      from: tru_totales
      to: DGCO
      tipo: requiere
    [564]
      from: tru_totales
      to: UI
      tipo: requiere
    [565]
      from: tru_totales
      to: CC
      tipo: requiere
    [566]
      from: tru_totales
      to: SC
      tipo: requiere
    [567]
      from: tru_totales
      to: CT
      tipo: requiere
    [568]
      from: tru_totales
      to: tru_totales.verificar
      tipo: declara_capacidad
    [569]
      from: tru_totales
      to: tru_totales.barrer
      tipo: declara_capacidad
    [570]
      from: tru_totales
      to: tru_totales.verificar_salida
      tipo: declara_capacidad
    [571]
      from: tru_totales
      to: tru_totales.categorias
      tipo: declara_capacidad
    [572]
      from: tru_totales
      to: tru_totales.capacidades
      tipo: declara_capacidad
    [573]
      from: tru_totales
      to: tru_totales.resolver_pedido
      tipo: declara_capacidad
    [574]
      from: tru_totales
      to: tru_totales.inventario
      tipo: declara_capacidad
    [575]
      from: tru_totales
      to: tru_totales.reporte
      tipo: declara_capacidad
    [576]
      from: tru_totales
      to: tru_totales.diagnostico
      tipo: declara_capacidad
    [577]
      from: tru_totales
      to: tru_totales.ejecutar_total
      tipo: declara_capacidad
    [578]
      from: tru_totales
      to: tru_totales.inspeccionar
      tipo: declara_capacidad
    [579]
      from: tru_totales
      to: tru_totales.registrar_inventario
      tipo: declara_capacidad
    [580]
      from: tru_totales
      to: tru_totales.evaluar_universal
      tipo: declara_capacidad
    [581]
      from: verificacion
      to: CE
      tipo: requiere
    [582]
      from: verificacion
      to: AX
      tipo: requiere
    [583]
      from: verificacion
      to: FO
      tipo: requiere
    [584]
      from: verificacion
      to: MC
      tipo: requiere
    [585]
      from: verificacion
      to: SF
      tipo: requiere
    [586]
      from: verificacion
      to: CA
      tipo: requiere
    [587]
      from: verificacion
      to: CX
      tipo: requiere
    [588]
      from: verificacion
      to: DI
      tipo: requiere
    [589]
      from: verificacion
      to: RE
      tipo: requiere
    [590]
      from: verificacion
      to: TX
      tipo: requiere
    [591]
      from: verificacion
      to: CH
      tipo: requiere
    [592]
      from: verificacion
      to: CIT
      tipo: requiere
    [593]
      from: verificacion
      to: DGCO
      tipo: requiere
    [594]
      from: verificacion
      to: UI
      tipo: requiere
    [595]
      from: verificacion
      to: CC
      tipo: requiere
    [596]
      from: verificacion
      to: TT
      tipo: requiere
    [597]
      from: verificacion
      to: SC
      tipo: requiere
    [598]
      from: verificacion
      to: CT
      tipo: requiere
    [599]
      from: verificacion
      to: verificacion.verificar
      tipo: declara_capacidad
    [600]
      from: verificacion
      to: verificacion.barrer
      tipo: declara_capacidad
    [601]
      from: verificacion
      to: verificacion.verificar_salida
      tipo: declara_capacidad
    [602]
      from: verificacion
      to: verificacion.axiomas
      tipo: declara_capacidad
    [603]
      from: verificacion
      to: verificacion.inventario
      tipo: declara_capacidad
    [604]
      from: verificacion
      to: verificacion.reporte
      tipo: declara_capacidad
    [605]
      from: verificacion
      to: verificacion.diagnostico
      tipo: declara_capacidad
    [606]
      from: verificacion
      to: verificacion.ejecutar_total
      tipo: declara_capacidad
    [607]
      from: verificacion
      to: verificacion.inspeccionar
      tipo: declara_capacidad
    [608]
      from: verificacion
      to: verificacion.registrar_inventario
      tipo: declara_capacidad
    [609]
      from: verificacion
      to: verificacion.evaluar_universal
      tipo: declara_capacidad

══════════════════════════════════════════════════════════════════════
  TRAZAS DE EJECUCIÓN
══════════════════════════════════════════════════════════════════════
  [0]
    id_traza: 1
    timestamp: 2026-08-20T07:43:52.758301+00:00
    modulo: axiomas
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.014928
  [1]
    id_traza: 2
    timestamp: 2026-08-20T07:43:52.772782+00:00
    modulo: axiomas
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.014402
  [2]
    id_traza: 3
    timestamp: 2026-08-20T07:43:52.786548+00:00
    modulo: axiomas
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.013677
  [3]
    id_traza: 4
    timestamp: 2026-08-20T07:43:52.786634+00:00
    modulo: cache
    capacidad: reporte
    estado: EXITO
    duracion_s: 2.3e-05
  [4]
    id_traza: 5
    timestamp: 2026-08-20T07:43:52.786708+00:00
    modulo: cache
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 1e-05
  [5]
    id_traza: 6
    timestamp: 2026-08-20T07:43:53.072154+00:00
    modulo: cache
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.285391
  [6]
    id_traza: 7
    timestamp: 2026-08-20T07:43:53.072928+00:00
    modulo: calculator
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.000706
  [7]
    id_traza: 8
    timestamp: 2026-08-20T07:43:53.073515+00:00
    modulo: calculator
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000551
  [8]
    id_traza: 9
    timestamp: 2026-08-20T07:43:53.074127+00:00
    modulo: calculator
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000566
  [9]
    id_traza: 10
    timestamp: 2026-08-20T07:43:53.075205+00:00
    modulo: capacidades_engine
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.001045
  [10]
    id_traza: 11
    timestamp: 2026-08-20T07:43:53.075490+00:00
    modulo: capacidades_engine
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000252
  [11]
    id_traza: 12
    timestamp: 2026-08-20T07:43:53.075943+00:00
    modulo: capacidades_engine
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000412
  [12]
    id_traza: 13
    timestamp: 2026-08-20T07:43:53.078339+00:00
    modulo: catalogo_citaciones
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.002363
  [13]
    id_traza: 14
    timestamp: 2026-08-20T07:43:53.079823+00:00
    modulo: catalogo_citaciones
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.001448
  [14]
    id_traza: 15
    timestamp: 2026-08-20T07:43:53.081291+00:00
    modulo: catalogo_citaciones
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.001424
  [15]
    id_traza: 16
    timestamp: 2026-08-20T07:43:53.081336+00:00
    modulo: citacion
    capacidad: reporte
    estado: EXITO
    duracion_s: 4e-06
  [16]
    id_traza: 17
    timestamp: 2026-08-20T07:43:53.081366+00:00
    modulo: citacion
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 1e-06
  [17]
    id_traza: 18
    timestamp: 2026-08-20T07:43:53.081394+00:00
    modulo: citacion
    capacidad: inventario
    estado: EXITO
    duracion_s: 5e-06
  [18]
    id_traza: 19
    timestamp: 2026-08-20T07:43:53.081998+00:00
    modulo: constante
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.000578
  [19]
    id_traza: 20
    timestamp: 2026-08-20T07:43:53.082155+00:00
    modulo: constante
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000117
  [20]
    id_traza: 21
    timestamp: 2026-08-20T07:43:53.082285+00:00
    modulo: constante
    capacidad: inventario
    estado: EXITO
    duracion_s: 9.5e-05
  [21]
    id_traza: 22
    timestamp: 2026-08-20T07:43:53.097332+00:00
    modulo: contexto
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.015014
  [22]
    id_traza: 23
    timestamp: 2026-08-20T07:43:53.098586+00:00
    modulo: contexto
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.001194
  [23]
    id_traza: 24
    timestamp: 2026-08-20T07:43:53.101865+00:00
    modulo: contexto
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.003235
  [24]
    id_traza: 25
    timestamp: 2026-08-20T07:43:53.138151+00:00
    modulo: correlacion_mecanica
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.036246
  [25]
    id_traza: 26
    timestamp: 2026-08-20T07:43:53.168511+00:00
    modulo: correlacion_mecanica
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.030308
  [26]
    id_traza: 27
    timestamp: 2026-08-20T07:43:53.195545+00:00
    modulo: correlacion_mecanica
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.026968
  [27]
    id_traza: 28
    timestamp: 2026-08-20T07:43:53.195618+00:00
    modulo: diagnosticoD
    capacidad: reporte
    estado: EXITO
    duracion_s: 4e-06
  [28]
    id_traza: 29
    timestamp: 2026-08-20T07:43:53.195649+00:00
    modulo: diagnosticoD
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 1e-06
  [29]
    id_traza: 30
    timestamp: 2026-08-20T07:43:53.195698+00:00
    modulo: diagnosticoD
    capacidad: inventario
    estado: EXITO
    duracion_s: 3e-06
  [30]
    id_traza: 31
    timestamp: 2026-08-20T07:43:53.199174+00:00
    modulo: diccionario
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.003451
  [31]
    id_traza: 32
    timestamp: 2026-08-20T07:43:53.199227+00:00
    modulo: diccionario
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 1.6e-05
  [32]
    id_traza: 33
    timestamp: 2026-08-20T07:43:53.199276+00:00
    modulo: diccionario
    capacidad: inventario
    estado: EXITO
    duracion_s: 1.6e-05
  [33]
    id_traza: 34
    timestamp: 2026-08-20T07:43:53.202457+00:00
    modulo: formulas
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.003156
  [34]
    id_traza: 35
    timestamp: 2026-08-20T07:43:53.203535+00:00
    modulo: formulas
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.001031
  [35]
    id_traza: 36
    timestamp: 2026-08-20T07:43:53.203940+00:00
    modulo: formulas
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000363
  [36]
    id_traza: 37
    timestamp: 2026-08-20T07:43:53.204005+00:00
    modulo: interfaz
    capacidad: inventario
    estado: EXITO
    duracion_s: 2.6e-05
  [37]
    id_traza: 38
    timestamp: 2026-08-20T07:43:53.207765+00:00
    modulo: realidad
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.00373
  [38]
    id_traza: 39
    timestamp: 2026-08-20T07:43:53.208390+00:00
    modulo: realidad
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000588
  [39]
    id_traza: 40
    timestamp: 2026-08-20T07:43:53.228108+00:00
    modulo: realidad
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.019674
  [40]
    id_traza: 41
    timestamp: 2026-08-20T07:43:53.238089+00:00
    modulo: self
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.009914
  [41]
    id_traza: 42
    timestamp: 2026-08-20T07:43:53.246662+00:00
    modulo: self
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.008519
  [42]
    id_traza: 43
    timestamp: 2026-08-20T07:43:53.246746+00:00
    modulo: self
    capacidad: inventario
    estado: EXITO
    duracion_s: 1e-05
  [43]
    id_traza: 44
    timestamp: 2026-08-20T07:43:53.268469+00:00
    modulo: spartaco_seguridad
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.021694
  [44]
    id_traza: 45
    timestamp: 2026-08-20T07:43:53.269136+00:00
    modulo: spartaco_seguridad
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000616
  [45]
    id_traza: 46
    timestamp: 2026-08-20T07:43:53.269746+00:00
    modulo: spartaco_seguridad
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000566
  [46]
    id_traza: 47
    timestamp: 2026-08-20T07:43:53.270931+00:00
    modulo: taxonomia
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.00115
  [47]
    id_traza: 48
    timestamp: 2026-08-20T07:43:53.271194+00:00
    modulo: taxonomia
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000228
  [48]
    id_traza: 49
    timestamp: 2026-08-20T07:43:53.271428+00:00
    modulo: taxonomia
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000196
  [49]
    id_traza: 50
    timestamp: 2026-08-20T07:43:53.273261+00:00
    modulo: tru_totales
    capacidad: reporte
    estado: EXITO
    duracion_s: 0.001803
  [50]
    id_traza: 51
    timestamp: 2026-08-20T07:43:53.274105+00:00
    modulo: tru_totales
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 0.000811
  [51]
    id_traza: 52
    timestamp: 2026-08-20T07:43:53.274909+00:00
    modulo: tru_totales
    capacidad: inventario
    estado: EXITO
    duracion_s: 0.000766
  [52]
    id_traza: 53
    timestamp: 2026-08-20T07:43:53.274953+00:00
    modulo: verificacion
    capacidad: reporte
    estado: EXITO
    duracion_s: 7e-06
  [53]
    id_traza: 54
    timestamp: 2026-08-20T07:43:53.274981+00:00
    modulo: verificacion
    capacidad: diagnostico
    estado: EXITO
    duracion_s: 1e-06
  [54]
    id_traza: 55
    timestamp: 2026-08-20T07:43:53.275007+00:00
    modulo: verificacion
    capacidad: inventario
    estado: EXITO
    duracion_s: 2e-06

══════════════════════════════════════════════════════════════════════
  MAPA DE RUTA DE EJECUCIÓN
══════════════════════════════════════════════════════════════════════

══════════════════════════════════════════════════════════════════════
  CIERRE
══════════════════════════════════════════════════════════════════════
  Versión Omega : 12.2-puro
  Todo el contenido mostrado fue entregado por Engine.
  Omega no realizó cálculos.
  Fin del reporte.
══════════════════════════════════════════════════════════════════════

JSON: /home/runner/work/VPSI-TRUTH_1.1/VPSI-TRUTH_1.1/diagnostics/omega_report_data.json
