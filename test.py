from board import UltimateTicTacToe
from keras.models import load_model
import numpy as np

env = UltimateTicTacToe()
model = load_model("TTTAgent.h5")

state = np.fromstring("""0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 1.0, 0.0, 1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.5, 0.0, 0.5, 1.0, 0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 1.0, 1.0, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0, 0.5, 0.3333333333333333""", dtype = 'float', sep =",")
state = state.reshape(1,82)

print(model.predict(state))
