import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm


def expectation_step(x, mu, sigma, pi):
    # E步
    likelihood = np.zeros((n_samples, n_components))
    for k in range(n_components):
        likelihood[:, k] = norm.pdf(x, loc=mu[k], scale=sigma[k])
    weighted_likelihood = likelihood * pi
    total_weighted_likelihood = np.sum(weighted_likelihood, axis=1)
    responsibilities = weighted_likelihood / total_weighted_likelihood[:, np.newaxis]
    return responsibilities


def maximization_step(x, responsibilities):
    # M步
    total_responsibilities = np.sum(responsibilities, axis=0)
    pi = total_responsibilities / n_samples
    mu = np.sum(responsibilities * x[:, np.newaxis], axis=0) / total_responsibilities
    sigma = np.sqrt(np.sum(responsibilities * (x[:, np.newaxis] - mu) ** 2, axis=0) / total_responsibilities)
    return mu, sigma, pi

def predict(X, pi, mu, sigma):
    # 预测
    K = len(pi)
    gamma = np.zeros((np.size(X,0), K))
    for k in range(K):
        gamma[:, k] = pi[k] * norm.pdf(X, mu[k], sigma[k])
    return gamma.argmax(axis=1)

if __name__ == '__main__':

    # 读取数据
    data = pd.read_csv('height_data.csv')
    heights = data['height'].values
    # 设定初始参数
    n_components = 2
    n_samples = len(heights)
    mu = np.random.choice(heights, n_components)
    sigma = np.ones(n_components)
    pi = np.ones(n_components) / n_components
    print("Initial means:", mu)
    print("Initial standard deviations:", sigma)
    print("Initial weights:", pi)

    max_iter = 300      #最大迭代次数
    pi_plot = []
    mu_plot = []
    sigma_plot = []

    for i in range(max_iter):
        responsibilities = expectation_step(heights, mu, sigma, pi)
        mu_new, sigma_new, pi_new = maximization_step(heights, responsibilities)

        mu, sigma, pi = mu_new, sigma_new, pi_new
        pi_plot.append(pi)
        mu_plot.append(mu)
        sigma_plot.append(sigma)

    print("Final means:", mu)
    print("Final standard deviations:", sigma)
    print("Final weights:", pi)

    x = np.linspace(150, 200, 4000)
    y = pi[0] * norm.pdf(x, mu[0], sigma[0]) + pi[1] * norm.pdf(x, mu[1], sigma[1])
    plt.hist(data, bins=50, density=True, alpha=0.5)
    plt.plot(x, y)
    plt.show()
    #pi mu sigma随着迭代的变化
    plt.plot(pi_plot)
    plt.xlabel("Iteration")
    plt.ylabel("pi")
    plt.legend(['pi1', 'pi2'])
    plt.show()

    plt.plot(mu_plot)
    plt.xlabel("Iteration")
    plt.ylabel("mu")
    plt.legend(['mu1', 'mu2'])
    plt.show()

    plt.plot(sigma_plot)
    plt.xlabel("Iteration")
    plt.ylabel("sigma")
    plt.legend(['sigma1', 'sigma2'])
    plt.show()
    # 预测
    pred = predict(heights, pi, mu, sigma)
    print(('Prediction Result',pred))