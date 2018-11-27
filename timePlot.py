import pickle
from dcel import DCEL, Vertex, HalfEdge, Face
from mapOverlay import MapOverlay
from matplotlib import pyplot as plt

nums = [10, 40, 70, 100, 130, 160, 190, 220, 250, 280]
def reader(num_vertices):
    with open('D:\\remake\\intersection\\'+str(num_vertices) + '_vertex_overlay.p', 'rb') as f_:
        dcel = pickle.load(f_)

    for d in dcel:
        for v in d.vertices:
            v.coordinates = tuple(v.coordinates.tolist())

    f = MapOverlay()
    _, time = f.calculate(dcel[0], dcel[1])
    return time

if __name__ == "__main__":
    times = []
    for num in nums:
        times.append(reader(num))
    plt.scatter(nums, times, c='#FF0090')
    plt.title('Run time plot')
    plt.xlabel('Number of vertices')
    plt.ylabel('Run time (s)')
    plt.show()