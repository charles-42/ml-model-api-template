import onnxruntime as rt
import numpy as np
import pandas as pd

sess = rt.InferenceSession("best_reg_lin_produit_recu.onnx")

produit_recu = input("Avez reçu votre produit?")

if produit_recu == "oui":
    produit_recu = 1
else:
    produit_recu = 0

temps_livraison = 0  # valeur par défaut 

data = np.array([produit_recu, temps_livraison], dtype=np.float32).reshape(1, 2)

input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name

prediction = sess.run([label_name], {input_name: data})[0]

if prediction[0]==1:
    print("Alors vous devez être content")
else:
    print("Je suppose que vous êtes frustré")
