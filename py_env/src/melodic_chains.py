from music_environment import MusicEnvironment
import markov_chain


def main():
	selected_order = 1
	directory_path = "../../melodies/classical/bach"
	transition_probs = markov_chain.get_markov_chain(directory_path, order=selected_order)
	
	env = MusicEnvironment(('localhost', 5555))
	for i in range(10):
		agent = ComposerAgent(env, transition_probs)

	# Audience agents also?

	sim = Simulation(env, log_folder='logs', callback=env.vote) # MusicEnvironment.vote is missing as of now.
	sim.async_steps(10)
	sim.end()

if __name__ == "__main__":
	main()
	