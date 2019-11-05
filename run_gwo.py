from env_gwo import EGWO

def F1_05(x):
    val = sum(x ** 2)
    return val

if __name__ == "__main__":
    func = F1_05
    min_bound = -100
    max_bound = 100
    dimension = 30
    n_point = 10
    iteration = 1000
    env = EGWO(func, min_bound, max_bound, dimension, n_point, iteration)
    env.move()

    # m_RL = PolicyGradient(
    #     n_actions = env._get_action_len(),
    #     n_features = env._get_state_len(),
    #     learning_rate = 0.02,
    #     reward_decay = 0.99,
    #     # output_graph=True,
    # )