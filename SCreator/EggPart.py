import pandas as pd


class EggSample:
    def __init__(self, part_class, number, ill):
        self.data = pd.DataFrame
        self.part_class = part_class
        self.number = number
        self.ill = ill

    def integrate_over_range(self, x_start, x_end):
        result = 0
        s = self.data["wavelength"]
        for index, value in s.items():
            if x_start <= value <= x_end:
                result += self.data["reflectance"][index]
        return result

    def calculate_slope(self, x_start, x_end):
        s = self.data["wavelength"]
        cnt_index = 0
        p1 = -10000
        for index, value in s.items():
            if x_start <= value <= x_end and cnt_index == 0:
                p1 = self.data["reflectance"][index]
            if x_start <= value <= x_end:
                cnt_index = index + 1
        p2 = self.data["reflectance"][cnt_index-1]
        return (p2 - p1) / (x_end - x_start)


class EggPart:
    def __init__(self):
        self.samples = []

    def add_sample(self, egg_sample: EggSample):
        self.samples.append(egg_sample)

    def set_samples(self, sample: list):
        self.samples = sample

    def average_for_samples(self, x_start, x_end):
        averaged_result = 0
        for sample in self.samples:
            averaged_result += sample.integrate_over_range(x_start, x_end)
        averaged_result /= len(self.samples)
        return averaged_result

    # checking if any of the samples isn't an outlier
    def find_outliers(self):
        # dobra tutaj porownam sb usrednia calke do kazdej calki i najwyzej wywale te odchylki i bedzie gites
        # jak cos to jakies Z albo idk odchylenie standardowe no klasyczek polecimy
        pass
