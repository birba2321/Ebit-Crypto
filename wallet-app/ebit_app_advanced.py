import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import time
import random
import hashlib

# Blockchain semplificata per Ebit
class Block:
    def __init__(self, index, previous_hash, timestamp, data, reward):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.reward = reward
        self.nonce, self.hash = self.mine_block()

    def calculate_hash(self, nonce):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        nonce = random.randint(0, 1000)
        hash_result = self.calculate_hash(nonce)
        return nonce, hash_result

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.balance = {}
        self.history = []

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", reward=0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, miner, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            previous_hash=previous_block.hash,
            timestamp=time.time(),
            data=data,
            reward=0.01
        )
        self.chain.append(new_block)
        self.balance[miner] = self.balance.get(miner, 0) + new_block.reward
        self.history.append((len(self.chain)-1, self.balance[miner]))
        return new_block

    def get_balance(self, miner):
        return self.balance.get(miner, 0)

# Interfaccia grafica avanzata
class EbitAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.blockchain = Blockchain()
        self.miner = "Elena"
        self.mining = False

        # Dashboard saldo
        self.label_balance = Label(text=f"Saldo {self.miner}: 0 Ebit", font_size=20)
        self.add_widget(self.label_balance)

        # Pulsanti
        btn_layout = BoxLayout(size_hint_y=None, height=50)
        self.btn_start = Button(text="⛏️ Avvia Mining")
        self.btn_start.bind(on_press=self.start_mining)
        btn_layout.add_widget(self.btn_start)

        self.btn_stop = Button(text="🛑 Ferma Mining")
        self.btn_stop.bind(on_press=self.stop_mining)
        btn_layout.add_widget(self.btn_stop)

        self.add_widget(btn_layout)

        # Storico blocchi
        self.scroll = ScrollView(size_hint=(1, 0.4))
        self.history_layout = GridLayout(cols=1, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.scroll.add_widget(self.history_layout)
        self.add_widget(self.scroll)

        # Grafico ricompense
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Ricompense accumulate")
        self.ax.set_xlabel("Blocchi")
        self.ax.set_ylabel("Saldo Ebit")
        self.graph = FigureCanvasKivyAgg(self.fig)
        self.add_widget(self.graph)

    def start_mining(self, instance):
        self.mining = True
        Clock.schedule_interval(self.mine_block, 2)

    def stop_mining(self, instance):
        self.mining = False
        Clock.unschedule(self.mine_block)

    def mine_block(self, dt):
        if self.mining:
            block = self.blockchain.add_block(self.miner, f"{self.miner} mina un blocco")
            saldo = self.blockchain.get_balance(self.miner)
            self.label_balance.text = f"Saldo {self.miner}: {saldo:.2f} Ebit"

            # Aggiorna storico
            lbl = Label(text=f"Blocco #{block.index} | Reward: {block.reward} | Hash: {block.hash[:10]}...")
            self.history_layout.add_widget(lbl)

            # Aggiorna grafico
            self.ax.clear()
            self.ax.set_title("Ricompense accumulate")
            self.ax.set_xlabel("Blocchi")
            self.ax.set_ylabel("Saldo Ebit")
            x, y = zip(*self.blockchain.history)
            self.ax.plot(x, y, marker="o", color="green")
            self.graph.draw()

class EbitApp(App):
    def build(self):
        return EbitAppUI()

if __name__ == "__main__":
    EbitApp().run()
