import DECIMER

def predict(path):
    smiles = DECIMER.predict_SMILES(path)
    return smiles