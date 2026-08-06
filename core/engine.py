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
    # SECCIÓN AX — contrato modules/axiomas (CONTENEDOR v9.5)
    #
    # Origen: modules/axiomas/__init__.py
    # Rol: AX | nombre: axiomas
    #
    # Autorizacion:
    #   Todo lo que el CONTENEDOR de axiomas declara.
    #   Capacidades: verificar, barrer, inventario, axiomas, generatividad.
    #   El Engine no reimplementa contradicciones ni normalizacion:
    #   ejecuta las funciones del modulo por contrato.
    #
    # Contrato del modulo:
    #   - Vigila declaraciones (axioma|lema|teorema|corolario|definicion).
    #   - No calcula Tru_total.
    #   - No clasifica entrada O (eso es CX).
    #   - Fail-closed: si choques o errores de carga → coherente=False.
    # ===============================================================
    def _ax_contenedor(self) -> Optional[Contenedor]:
        return self.registro.primero("AX")

    def _ax_capacidad(self, capacidad: str, *args: Any, **kwargs: Any) -> Any:
        """
        Invoca una capacidad declarada en CONTENEDOR de axiomas.
        Solo lo que el contrato expone.
        """
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
                "razon": "capacidad no declarada en CONTENEDOR",
            })
            return None
        return self._ejecutar_capacidad(cont, capacidad, *args, **kwargs)

    def ax_barrer(
        self,
        declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Contrato: verificar / barrer.
        Coherencia del cuerpo axiomatico (choques + errores de carga).
        """
        out = self._ax_capacidad("barrer", declaraciones_externas)
        if isinstance(out, dict):
            self.informe_axiomas = out
            return out
        out = self._ax_capacidad("verificar", declaraciones_externas)
        if isinstance(out, dict):
            self.informe_axiomas = out
            return out
        return None

    def ax_axiomas(
        self,
        declaraciones_externas: Optional[Dict[str, List[Dict]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Contrato: axiomas.
        Lista normalizada si el cuerpo es coherente; si no → [].
        """
        out = self._ax_capacidad("axiomas", declaraciones_externas)
        return list(out) if isinstance(out, list) else []

    def ax_inventario(self, peticion: Any = None) -> Optional[Dict[str, Any]]:
        """Contrato: inventario — mapa del modulo axiomas."""
        out = self._ax_capacidad("inventario", peticion)
        return out if isinstance(out, dict) else None

    def ax_generatividad(self) -> Optional[Dict[str, Any]]:
        """
        Contrato: generatividad.
        TR1 operativa + canonica sobre el cuerpo cargado.
        No calcula Tru.
        """
        out = self._ax_capacidad("generatividad")
        return out if isinstance(out, dict) else None

    def _ax_compuerta(self) -> None:
        """
        Arranque: exige contenedor AX y cuerpo coherente.
        Usa solo barrer/verificar del contrato.
        """
        cont = self._ax_contenedor()
        if cont is None:
            self.errores_arranque.append(
                "AX: falta contenedor obligatorio (modules/axiomas)"
            )
            return

        informe = self.ax_barrer()
        if informe is None:
            self.errores_arranque.append(
                "AX/{0}: barrer/verificar no resolvio".format(cont.nombre)
            )
            return

        self.informe_axiomas = informe
        if not informe.get("coherente", False):
            n_choques = len(informe.get("choques") or [])
            n_errores = len(informe.get("errores") or [])
            self.errores_arranque.append(
                "AX/{0}: incoherente choques={1} errores={2}".format(
                    cont.nombre, n_choques, n_errores
                )
            )
