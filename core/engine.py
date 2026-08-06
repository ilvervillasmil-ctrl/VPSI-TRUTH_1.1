# -*- coding: utf-8 -*-
"""
VPSI-TRUTH --- core/engine.py
Version 12.0

Descripcion
  El Engine es el nucleo del repositorio. Integra los modulos del sistema
  a partir de los contratos que cada uno declara en su CONTENEDOR.

  Estructura
    Una seccion del Engine por modulo/rol.
    Cada seccion se construye desde el __init__ y el CONTENEDOR de ese modulo.
    La seccion queda autorizada a todo lo que ese modulo declara y contiene.
    El contrato de la seccion es el contrato del modulo.

  Que hace
    - Descubre cada carpeta de modulo y lee su __init__.
    - Registra el CONTENEDOR (rol, capacidades, requiere, version).
    - Conecta las capacidades declaradas.
    - Calcula e invoca mediante esas capacidades: lo que el modulo permite,
      el Engine lo puede usar (C, L, K, Tru, marco, mandatos, etc.).
    - No inventa oficios fuera del contrato.
    - No sustituye la logica interna del modulo: la ejecuta por contrato.

  Principio
    El conocimiento y la logica viven en cada modulo.
    El Engine activa lo que cada contrato autoriza.
    Nuevos modulos o roles = nuevas secciones, sin reescribir el resto.
"""

    # ===============================================================
    # SECCIÓN: AX
    # ===============================================================
    #
    # Contrato origen : modules/axiomas/__init__.py
    # nombre          : axiomas
    # rol             : AX
    # version         : 9.5
    # requiere        : []
    # capacidades     : verificar, barrer, inventario, axiomas, generatividad
    #
    # Autoridad de engine sobre este modulo:
    #   - Lee el CONTENEDOR de modules/axiomas/
    #   - Lee absolutamente TODOS los archivos bajo modules/axiomas/
    #   - Ejecuta todas las capacidades que el CONTENEDOR declara
    #   - No inventa oficios. No sustituye la logica del modulo.
    #   - No calcula Tru_total. No clasifica O de entrada.
    #
    # Prueba:
    #   Esta seccion se valida directamente contra modules/axiomas/
    #
    # ---------------------------------------------------------------
    # subsección: metadatos del contrato
    # ---------------------------------------------------------------
    AX_CONTRATO = {
        "nombre": "axiomas",
        "rol": "AX",
        "version": "9.5",
        "requiere": [],
        "capacidades": (
            "verificar",
            "barrer",
            "inventario",
            "axiomas",
            "generatividad",
        ),
        "carpeta": "modules/axiomas",
    }

    # ---------------------------------------------------------------
    # subsección: contenedor
    # ---------------------------------------------------------------
    def _ax_contenedor(self) -> Optional[Contenedor]:
        return self.registro.primero("AX")

    # ---------------------------------------------------------------
    # subsección: todos los archivos del modulo
    # ---------------------------------------------------------------
    def _ax_archivos(self) -> List[str]:
        """
        Lee absolutamente TODOS los archivos bajo modules/axiomas/.
        Autoridad total de Angie sobre el contenido de la carpeta.
        """
        cont = self._ax_contenedor()
        if cont is None:
            return []
        dir_mod = Path(cont.ruta).resolve().parent
        return sorted(
            str(p.relative_to(dir_mod))
            for p in dir_mod.rglob("*")
            if p.is_file()
        )

    # ---------------------------------------------------------------
    # subsección: invocacion por contrato
    # ---------------------------------------------------------------
    def _ax_capacidad(self, capacidad: str, *args: Any, **kwargs: Any) -> Any:
        """
        Ejecuta una capacidad declarada en el CONTENEDOR de axiomas.
        Solo lo que el contrato autoriza.
        """
        if capacidad not in self.AX_CONTRATO["capacidades"]:
            self.fallos.append({
                "seccion": "AX",
                "capacidad": capacidad,
                "razon": "capacidad fuera del CONTENEDOR de axiomas",
            })
            return None

        cont = self._ax_contenedor()
        if cont is None:
            self.fallos.append({
                "seccion": "AX",
                "capacidad": capacidad,
                "razon": "rol AX sin contenedor cargado",
            })
            return None

        if not cont.tiene(capacidad):
            self.fallos.append({
                "seccion": "AX",
                "contenedor": cont.nombre,
                "capacidad": capacidad,
                "razon": "capacidad no resoluble en el modulo",
            })
            return None

        return self._ejecutar_capacidad(cont, capacidad, *args, **kwargs)

    # ---------------------------------------------------------------
    # subsección: capacidad — barrer
    # ---------------------------------------------------------------
    def ax_barrer(
        self,
        declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
    ) -> Optional[Dict[str, Any]]:
        """CONTENEDOR.capacidades['barrer'] → barrer()"""
        out = self._ax_capacidad("barrer", declaraciones_externas)
        if isinstance(out, dict):
            self.informe_axiomas = out
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: capacidad — verificar
    # ---------------------------------------------------------------
    def ax_verificar(
        self,
        declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
    ) -> Optional[Dict[str, Any]]:
        """CONTENEDOR.capacidades['verificar'] → barrer()"""
        out = self._ax_capacidad("verificar", declaraciones_externas)
        if isinstance(out, dict):
            self.informe_axiomas = out
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: capacidad — axiomas
    # ---------------------------------------------------------------
    def ax_axiomas(
        self,
        declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
    ) -> List[Dict[str, Any]]:
        """CONTENEDOR.capacidades['axiomas'] → axiomas()"""
        out = self._ax_capacidad("axiomas", declaraciones_externas)
        if isinstance(out, list):
            return out
        return []

    # ---------------------------------------------------------------
    # subsección: capacidad — inventario
    # ---------------------------------------------------------------
    def ax_inventario(self, peticion: Any = None) -> Optional[Dict[str, Any]]:
        """CONTENEDOR.capacidades['inventario'] → inventario()"""
        out = self._ax_capacidad("inventario", peticion)
        if isinstance(out, dict):
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: capacidad — generatividad
    # ---------------------------------------------------------------
    def ax_generatividad(self) -> Optional[Dict[str, Any]]:
        """CONTENEDOR.capacidades['generatividad'] → generatividad()"""
        out = self._ax_capacidad("generatividad")
        if isinstance(out, dict):
            return out
        return None

    # ---------------------------------------------------------------
    # subsección: compuerta de arranque
    # ---------------------------------------------------------------
    def _ax_compuerta(self) -> None:
        """
        Arranque AX contra modules/axiomas/:
          1. Contenedor presente.
          2. Archivos de la carpeta legibles.
          3. barrer/verificar resuelve.
          4. coherente=True (fail-closed del modulo).
        """
        cont = self._ax_contenedor()
        if cont is None:
            self.errores_arranque.append(
                "AX: falta contenedor obligatorio (modules/axiomas)"
            )
            return

        archivos = self._ax_archivos()
        if not archivos:
            self.errores_arranque.append(
                "AX/{0}: carpeta sin archivos legibles".format(cont.nombre)
            )

        informe = self.ax_barrer()
        if informe is None:
            informe = self.ax_verificar()

        if informe is None:
            self.errores_arranque.append(
                "AX/{0}: barrer/verificar no resolvio".format(cont.nombre)
            )
            return

        self.informe_axiomas = informe

        if not informe.get("coherente", False):
            self.errores_arranque.append(
                "AX/{0}: incoherente choques={1} errores={2}".format(
                    cont.nombre,
                    len(informe.get("choques") or []),
                    len(informe.get("errores") or []),
                )
            )

    # ===============================================================
    # FIN SECCIÓN: AX
    # ===============================================================
