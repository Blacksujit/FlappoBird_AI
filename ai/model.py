import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras.optimizers import Adam

class FlappyBirdAI:
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        model = Sequential([
            Conv2D(16, (3, 3), activation='relu', input_shape=(120, 160, 1)),  # Reduced number of filters
            Flatten(),
            Dense(64, activation='relu'),  # Reduced number of neurons
            Dense(2, activation='softmax')  # Jump or Do nothing
        ])
        model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def train(self, states, actions):
        self.model.fit(states, actions, epochs=10, validation_split=0.2)

    def predict(self, state):
        state = np.array(state)
        if state.ndim == 3:
            state = np.expand_dims(state, axis=0)
        return self.model.predict(state)

    def load_model(self, model_path):
        self.model.load_weights(model_path)

    def save_model(self, model_path):
        self.model.save_weights(model_path)
