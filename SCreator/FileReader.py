import pandas as pd
import logging
from datetime import datetime
import os
import numpy as np
from SCreator import EggPart

log_path = "logs/log"
logging.basicConfig(filename="{}_{}.log".format(log_path, datetime.now().strftime("%m-%d-%Y-%H_%M_%S")),
                    format='%(levelname)s : %(asctime)s : %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def create_egg_group(epart : dict) -> list:
    egg_parts = []

    for v in epart.values():
        ep = EggPart.EggPart()
        ep.set_samples(v)
        egg_parts.append(ep)
    return egg_parts


class FileReader:
    def __init__(self, dir_path: str):
        self.dir_path = dir_path

    @staticmethod
    def repair_columns_headers(df: pd.DataFrame()) -> pd.DataFrame:
        if df["wavelength"][2] == 3.0:
            df["wavelength"] = pd.read_csv("wavelengths.csv", header=None)
        return df

    def load_file(self, path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(path, sep=',', names=['wavelength', 'reflectance'],
                             dtype={'High': np.float64, 'Low': np.float64})
            df = self.repair_columns_headers(df)
            return df
        except pd.errors.EmptyDataError:
            logger.error('Problem with reading the file with pandas')

    def read_files(self):
        """
        Read data for each file in the directory and concatenate it.
        """
        try:
            paths = [f for f in os.listdir(self.dir_path)]
            try:
                egg_parts = {}
                for path in paths:
                    if path[-4::] in [".CSV", ".csv"] and path[-5:-4] not in [')']:
                        class_group = path.split("_")[2]
                        if path[0:7] == "Healthy":
                            ill = False
                        else:
                            ill = True
                        smp = EggPart.EggSample(class_group, int(path[-5:-4]), ill)
                        smp.data = self.load_file(self.dir_path + "/" + path)
                        if class_group in egg_parts.keys():
                            egg_parts[class_group].append(smp)
                        else:
                            egg_parts[class_group] = [smp]
                return create_egg_group(egg_parts)

            except ValueError as ve:
                logger.error(str(ve) + self.dir_path)
        except FileNotFoundError as e:
            logger.error(e)
