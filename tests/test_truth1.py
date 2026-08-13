"""
===============================================================================
TEST DE CAPACIDAD CONTRACTUAL — CÁLCULO DE VERDAD POR EL ENGINE
===============================================================================

PROPOSICIÓN QUE SE DEMUESTRA
----------------------------
Dada una conversación semántica y un contexto válido, el Engine de
VPSI-TRUTH ejecuta autónomamente sus contratos existentes y publica
las cuantificaciones deterministas Tru_Ri y Tru_total.

AUTORIDAD DE EJECUCIÓN
----------------------
El único punto de ejecución del cálculo es:

    resultado = engine.evaluar(peticion)

El test no calcula.
El test no orquesta módulos.
El test no reconstruye la cadena interna.
El test no conoce el número correcto.
El test solo entrega material semántico y observa el paquete contractual
que el Engine publica.

FÓRMULA CONTRACTUAL DE REFERENCIA (documental, no ejecutada aquí)
-----------------------------------------------------------------
    Tru_Ri    = C × L × K
    Tru_total = Tru_Ri × α + β

Estas fórmulas viven en los módulos productivos (FO / truth).
Este archivo no las implementa ni las importa.

PROHIBICIONES ABSOLUTAS EN ESTE ARCHIVO
---------------------------------------
- No importar Calculator, conteos, coherencia, logica, correlacion_k,
  truth.py, ALPHA, BETA ni ninguna fórmula.
- No fabricar O_id, permite_k, m, k, p, r, c, f, C, L, K.
- No hardcodear ningún valor numérico de Tru_Ri o Tru_total.
- No usar pytest.skip() para ocultar fallos de arranque.
- No usar strict=False.
- No aceptar PARCIAL / UNDEFINED / ERROR / RECHAZADO en el escenario
  principal (conversación + contexto suficiente).
- No modificar ningún módulo de producción.

===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# NOTA DE IMPLEMENTACIÓN — path del repositorio
# Se asume el layout estándar:
#   <repo>/
#     core/engine.py
#     modules/
#     tests/  ← este archivo
# Si el layout de tests/ es distinto, ajustar parents[N].
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# NOTA DE IMPLEMENTACIÓN — único import de producción permitido
# Solo se importa la interfaz pública del Engine.
# es_undefined se usa únicamente para inspeccionar la forma del valor
# publicado por el propio Engine (contrato de UNDEFINED), no para calcular.
# ---------------------------------------------------------------------------
from core.engine import Engine, es_undefined


# ===========================================================================
# MATERIAL SEMÁNTICO DE ENTRADA
# ===========================================================================
# NOTA: Estos textos son DATOS, no reglas de programación.
# No existe ninguna condición del tipo if "Carlos" in texto.
# El Engine debe tratarlos como material semántico puro.

CONVERSACION_A = (
    "Carlos: Mana, voy a Miami.\n"
    "Maria: Genial, ¿qué harás?\n"
    "Carlos: Voy de vacaciones. Tengo 5 apartamentos.\n"
    "Maria: Carlos me dijo que tiene 5 apartamentos.\n"
    "Carla: Yo soy la hermana. Esta es la evidencia: aquí están los "
    "contratos y títulos de propiedad de esos 5 apartamentos y son míos, "
    "no de Carlos."
)

CONVERSACION_B = (
    "Carlos: Mana, voy a Miami.\n"
    "Maria: Genial, ¿qué harás?\n"
    "Carlos: Voy de vacaciones. Tengo 5 apartamentos.\n"
    "Maria: Carlos me dijo que tiene 5 apartamentos.\n"
    "Carla: Yo soy la hermana. Aquí están los contratos y títulos de "
    "propiedad de los 5 apartamentos; están a nombre de Carlos."
)

CONVERSACION_NOMBRES = (
    "Pedro: Mana, voy a Miami.\n"
    "Laura: Genial, ¿qué harás?\n"
    "Pedro: Voy de vacaciones. Tengo 5 apartamentos.\n"
    "Laura: Pedro me dijo que tiene 5 apartamentos.\n"
    "Sofia: Yo soy la hermana. Esta es la evidencia: aquí están los "
    "contratos y títulos de propiedad de esos 5 apartamentos y son míos, "
    "no de Pedro."
)

# ---------------------------------------------------------------------------
# NOTA DE IMPLEMENTACIÓN — contexto
# Se entrega el contexto semántico como entrada.
# El Engine (vía CX y sus contratos) es quien debe resolver el dominio O.
# El test no construye O_id, no calcula permite_k, no genera registros
# internos. Solo declara: "esta es la afirmación y esta es la evidencia".
# ---------------------------------------------------------------------------

CONTEXTO_A = (
    "Afirmación a evaluar: Carlos afirma 'Tengo 5 apartamentos'. "
    "Evidencia aportada por Carla: los contratos y títulos de propiedad "
    "de esos 5 apartamentos están a su nombre y no a nombre de Carlos."
)

CONTEXTO_B = (
    "Afirmación a evaluar: Carlos afirma 'Tengo 5 apartamentos'. "
    "Evidencia aportada por Carla: los contratos y títulos de propiedad "
    "de esos 5 apartamentos están a nombre de Carlos."
)

CONTEXTO_NOMBRES = (
    "Afirmación a evaluar: Pedro afirma 'Tengo 5 apartamentos'. "
    "Evidencia aportada por Sofia: los contratos y títulos de propiedad "
    "de esos 5 apartamentos están a su nombre y no a nombre de Pedro."
)


# ===========================================================================
# CONSTRUCCIÓN DE PETICIÓN
# ===========================================================================

def _peticion(conversacion: str, contexto: str) -> dict:
    """
    NOTA DE IMPLEMENTACIÓN:
    Campos reconocidos por el contrato actual de Engine.evaluar /
    Engine._o_usable:
      texto, mensaje, descripcion, contexto, O_context, enunciado_O

    No se inyectan:
      C, L, K, m, k, p, r, c, f, O_id, permite_k, compromisos, etc.

    El Engine debe obtener esos valores mediante sus propios módulos.
    """
    return {
        "texto": conversacion,
        "mensaje": conversacion,
        "descripcion": conversacion,
        "contexto": contexto,
        "O_context": contexto,
        "enunciado_O": contexto,
        "escala_id": "tru_conversacion",
        "metodo": "operacional",
    }


def _peticion_sin_o(texto: str) -> dict:
    """
    NOTA DE IMPLEMENTACIÓN:
    Entrada deliberadamente sin dominio O.
    Se usa solo en el test de restricción contractual (Def-5.3.1).
    """
    return {
        "texto": texto,
        "mensaje": texto,
        "metodo": "operacional",
    }


# ===========================================================================
# INSPECCIÓN DE FORMA CONTRACTUAL PUBLICADA
# ===========================================================================

def _es_cuantificacion_publicada(valor) -> bool:
    """
    NOTA DE IMPLEMENTACIÓN:
    Verifica únicamente la forma del valor que el Engine publica:
      - no es None
      - no es el sentinel UNDEFINED del Engine
      - no es la cadena "UNDEFINED" / "NONE"
      - es convertible a Fraction (representación racional contractual)

    Esta función NO calcula la verdad.
    NO aplica la fórmula Tru_Ri = C×L×K.
    NO conoce el número correcto.
    Solo comprueba que el Engine publicó una cuantificación racional.
    """
    if valor is None:
        return False
    if es_undefined(valor):
        return False
    texto = str(valor).strip()
    if not texto or texto.upper() in ("UNDEFINED", "NONE"):
        return False
    try:
        from fractions import Fraction
        Fraction(texto)
        return True
    except Exception:
        return False


# ===========================================================================
# FIXTURE — Engine en configuración contractual real
# ===========================================================================

@pytest.fixture(scope="module")
def engine():
    """
    NOTA DE IMPLEMENTACIÓN:
    - strict=True  → cualquier incumplimiento de arranque falla el test.
    - verificar_axiomas=True → se ejecuta la ruta contractual normal.
    - No se usa pytest.skip(). Si el Engine no arranca, el CI falla.
    """
    raiz = ROOT / "modules"
    eng = Engine(
        raiz_modulos=raiz,
        invocador_id="test_calculo_verdad_contractual",
        verificar_axiomas=True,
        strict=True,
    )
    # Si el estado no es OPERATIVO, el assert falla el test (no se salta).
    assert eng.estado == "OPERATIVO", (
        "Engine no operativo. "
        f"estado={eng.estado!r} errores={eng.errores_arranque!r}"
    )
    return eng


# ===========================================================================
# TESTS
# ===========================================================================

class TestCapacidadCalculoVerdad:
    """
    NOTA DE DISEÑO DE LA SUITE
    --------------------------
    TEST A  — cálculo completo (evidencia contra)
    TEST B  — evidencia invertida (evaluación independiente)
    TEST C  — independencia de nombres
    TEST D  — determinismo (misma entrada → misma cuantificación)
    TEST E  — ausencia de O (restricción contractual separada)

    Los tests A-D exigen cuantificación.
    El test E exige la restricción de indefinición.
    """

    # ------------------------------------------------------------------
    # TEST A — Caso principal: cálculo completo de verdad
    # ------------------------------------------------------------------
    def test_a_calculo_completo_con_evidencia_contra(self, engine):
        """
        NOTA DE IMPLEMENTACIÓN:
        Entrada con conversación + contexto suficiente.
        El Engine debe ejecutar su cadena contractual y publicar:
          - estado == "OK"
          - Tru_Ri cuantificado
          - Tru_total cuantificado

        Cualquier otro estado (PARCIAL, UNDEFINED, ERROR, RECHAZADO)
        o la ausencia de cuantificación constituye FAIL.
        No se acepta la existencia de un diccionario como sustituto
        del cálculo de verdad.
        """
        pet = _peticion(CONVERSACION_A, CONTEXTO_A)
        resultado = engine.evaluar(pet)

        # Forma mínima del paquete
        assert isinstance(resultado, dict), (
            "Engine.evaluar debe devolver un dict contractual"
        )

        # Estado obligatorio para entrada con condiciones suficientes
        assert resultado.get("estado") == "OK", (
            "Con conversación + contexto suficiente se exige estado OK. "
            f"Recibido estado={resultado.get('estado')!r} "
            f"razon={resultado.get('razon')!r}"
        )

        # Publicación de las cuantificaciones contractuales
        assert "tru_ri" in resultado, (
            "El Engine debe publicar el campo contractual 'tru_ri'"
        )
        assert "tru_total" in resultado, (
            "El Engine debe publicar el campo contractual 'tru_total'"
        )

        assert _es_cuantificacion_publicada(resultado["tru_ri"]), (
            "Tru_Ri debe ser una cuantificación racional publicada. "
            f"Valor recibido: {resultado.get('tru_ri')!r}"
        )
        assert _es_cuantificacion_publicada(resultado["tru_total"]), (
            "Tru_total debe ser una cuantificación racional publicada. "
            f"Valor recibido: {resultado.get('tru_total')!r}"
        )

        # Observabilidad de factores (publicados por el Engine, no calculados aquí)
        assert "factores" in resultado, (
            "El Engine debe publicar el campo 'factores'"
        )
        assert isinstance(resultado["factores"], dict)

    # ------------------------------------------------------------------
    # TEST B — Evidencia invertida
    # ------------------------------------------------------------------
    def test_b_evidencia_invertida(self, engine):
        """
        NOTA DE IMPLEMENTACIÓN:
        Misma afirmación, evidencia opuesta.
        Se exige una evaluación independiente y cuantificada.
        El test NO conoce ni impone el número correcto.
        Solo exige que el Engine ejecute de nuevo la capacidad de cálculo
        y publique Tru_Ri / Tru_total cuantificados.
        """
        pet = _peticion(CONVERSACION_B, CONTEXTO_B)
        resultado = engine.evaluar(pet)

        assert isinstance(resultado, dict)
        assert resultado.get("estado") == "OK", (
            "Evidencia invertida también debe producir estado OK. "
            f"Recibido: {resultado.get('estado')!r}"
        )
        assert _es_cuantificacion_publicada(resultado.get("tru_ri")), (
            f"Tru_Ri no cuantificado: {resultado.get('tru_ri')!r}"
        )
        assert _es_cuantificacion_publicada(resultado.get("tru_total")), (
            f"Tru_total no cuantificado: {resultado.get('tru_total')!r}"
        )

    # ------------------------------------------------------------------
    # TEST C — Independencia de nombres (anti-hardcoding)
    # ------------------------------------------------------------------
    def test_c_independencia_de_nombres(self, engine):
        """
        NOTA DE IMPLEMENTACIÓN:
        Misma estructura semántica, identidades distintas
        (Pedro / Laura / Sofia).
        Si el Engine depende de los nombres literales "Carlos"/"Carla",
        este test debe fallar.
        Se exige cuantificación, no igualdad numérica con el caso A.
        """
        pet = _peticion(CONVERSACION_NOMBRES, CONTEXTO_NOMBRES)
        resultado = engine.evaluar(pet)

        assert isinstance(resultado, dict)
        assert resultado.get("estado") == "OK", (
            "Cambio de nombres no debe destruir la capacidad de evaluación. "
            f"Recibido: {resultado.get('estado')!r}"
        )
        assert _es_cuantificacion_publicada(resultado.get("tru_ri")), (
            f"Tru_Ri no cuantificado: {resultado.get('tru_ri')!r}"
        )
        assert _es_cuantificacion_publicada(resultado.get("tru_total")), (
            f"Tru_total no cuantificado: {resultado.get('tru_total')!r}"
        )

    # ------------------------------------------------------------------
    # TEST D — Determinismo
    # ------------------------------------------------------------------
    def test_d_determinismo(self, engine):
        """
        NOTA DE IMPLEMENTACIÓN:
        Misma petición ejecutada dos veces debe producir
        exactamente la misma cuantificación publicada.
        Esto no calcula la verdad; demuestra que el cálculo
        del Engine es determinista bajo entrada idéntica.
        """
        pet = _peticion(CONVERSACION_A, CONTEXTO_A)

        r1 = engine.evaluar(pet)
        r2 = engine.evaluar(pet)

        assert r1.get("estado") == "OK"
        assert r2.get("estado") == "OK"

        assert _es_cuantificacion_publicada(r1.get("tru_ri"))
        assert _es_cuantificacion_publicada(r1.get("tru_total"))
        assert _es_cuantificacion_publicada(r2.get("tru_ri"))
        assert _es_cuantificacion_publicada(r2.get("tru_total"))

        # Identidad de la cuantificación publicada
        assert str(r1["tru_ri"]) == str(r2["tru_ri"]), (
            "Dos ejecuciones idénticas deben publicar el mismo Tru_Ri. "
            f"r1={r1['tru_ri']!r} r2={r2['tru_ri']!r}"
        )
        assert str(r1["tru_total"]) == str(r2["tru_total"]), (
            "Dos ejecuciones idénticas deben publicar el mismo Tru_total. "
            f"r1={r1['tru_total']!r} r2={r2['tru_total']!r}"
        )

    # ------------------------------------------------------------------
    # TEST E — Ausencia de O (restricción contractual separada)
    # ------------------------------------------------------------------
    def test_e_sin_o_no_cuantifica(self, engine):
        """
        NOTA DE IMPLEMENTACIÓN:
        Caso contractual distinto (Def-5.3.1).
        Sin O usable el Engine no debe fabricar K ni publicar
        Tru_total cuantificado.
        Este test NO suaviza los tests A-D.
        """
        resultado = engine.evaluar(
            _peticion_sin_o("Tengo 5 apartamentos.")
        )

        assert isinstance(resultado, dict)

        estado = str(resultado.get("estado", "")).upper()
        assert estado == "UNDEFINED", (
            "Sin O usable se exige estado UNDEFINED. "
            f"Recibido: {estado!r}"
        )

        # No debe publicarse una cuantificación fabricada
        assert not _es_cuantificacion_publicada(resultado.get("tru_total")), (
            "Sin O no debe publicarse Tru_total cuantificado. "
            f"Valor recibido: {resultado.get('tru_total')!r}"
        )
        assert not _es_cuantificacion_publicada(resultado.get("tru_ri")), (
            "Sin O no debe publicarse Tru_Ri cuantificado. "
            f"Valor recibido: {resultado.get('tru_ri')!r}"
        )


# ===========================================================================
# Ejecución directa
# ===========================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
