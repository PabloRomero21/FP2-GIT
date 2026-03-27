# Estructura jerárquica de la AEI (Actualizada y Completa)
ESTRUCTURA_AEI = {
    "Ciencias Matemáticas, Físicas, Químicas e Ingenierías": {
        "Ciencias Matemáticas (MTM)": ["MTM", "MFU"],
        "Ciencias Físicas (FIS)": ["FYA", "ESP", "AYA", "FPN", "FAB", "FCM"],
        "Ciencias y Tecnologías Químicas (CTQ)": ["QMC", "IQM"],
        "Ciencias y Tecnologías de Materiales (MAT)": ["MAT", "MBM", "MEN", "MES", "MFU"],
        "Producción Ind., Ing. Civil e Ing. Sociedad (PIN)": ["PIN", "DPI", "ICA", "IBI", "IEA", "INA"],
        "Tecnologías de la Inf. y Comunicaciones (TIC)": ["INF", "MNF", "TCO"],
        "Energía y Transporte (EYT)": ["ENE", "TRA", "EYT"]
    },
    "Ciencias de la Vida": {
        "Biociencias y Biotecnología (BIO)": ["BMC", "BIO", "BIF", "BTC"],
        "Ciencias Agrarias y Agroalimentarias (CAA)": ["AGA", "ALI", "AYF", "GYA"],
        "Ciencias y Tecnologías Medioambientales (CTM)": ["CTM", "BOS", "MAR", "BVA", "BDV", "CTA", "CYA", "POL", "TMA"],
        "Biomedicina (BME)": ["BME", "FAR", "DMO", "CAN", "ESN", "DPT", "FOS", "IIT"]
    },
    "Ciencias Sociales y Humanidades": {
        "Derecho (DER)": ["DER"],
        "Economía (ECO)": ["ECO", "EYF", "EMA"],
        "Ciencias Sociales (CSO)": ["CSO", "SOC", "CPO", "GUR", "FEM", "GEO", "COM"],
        "Psicología (PSI)": ["PSI"],
        "Ciencias de la Educación (EDU)": ["EDU"],
        "Estudios del Pasado: Historia y Arqueología (PHA)": ["PHA", "HIS", "ARQ"],
        "Arte, Filología, Lingüística y Literatura (AFL)": ["ART", "LFL", "MLP", "FLL", "FIL", "LYL"]
    }
}

# Esta función "aplana" el diccionario para que la búsqueda sea instantánea
def obtener_mapa_subareas() -> dict:
    mapa_plano = {}
    for macroarea, areas in ESTRUCTURA_AEI.items():
        for area, subareas in areas.items():
            for subarea in subareas:
                # OJO: Guardamos en mayúsculas para evitar errores tipográficos del Excel
                mapa_plano[subarea.upper()] = {
                    "area": area,
                    "macroarea": macroarea
                }
    return mapa_plano