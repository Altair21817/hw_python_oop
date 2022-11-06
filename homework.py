"""
Программа фитнесс-ассистента.
Разработана Altair21817.
Все права не защищены.
"""

from typing import Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает Информационное сообщение."""
        # Определяет обязательно количество знаков после точки в числах float:
        ACCURACY: int = 3
        training_type: str = self.training_type

        message: str = (f'Тип тренировки: {training_type}; '
                        f'Длительность: {self.duration:.{ACCURACY}f} ч.; '
                        f'Дистанция: {self.distance:.{ACCURACY}f} км; '
                        f'Ср. скорость: {self.speed:.{ACCURACY}f} км/ч; '
                        f'Потрачено ккал: {self.calories:.{ACCURACY}f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self,
                 action_pcs: float,
                 duration_h: float,
                 weight_kg: float,
                 *args: list
                 ) -> None:
        # Получает данные в ед.изм "шт.":
        self.action_pcs: float = action_pcs
        # Получает данные в ед.изм "ч.":
        self.duration_h: float = duration_h
        # Получает данные в ед.изм "кг":
        self.weight_kg: float = weight_kg

    def get_distance(self) -> float:
        """Возвращает дистанцию в км."""
        distance_km: float = self.action_pcs * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость движения."""
        distance_km: float = self.get_distance()
        mean_speed_kmph: float = distance_km / self.duration_h
        return mean_speed_kmph

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training: InfoMessage = InfoMessage(type(self).__name__,
                                            self.duration_h,
                                            self.get_distance(),
                                            self.get_mean_speed(),
                                            self.get_spent_calories())
        return training


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        spent_calories_kkal: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                      * self.get_mean_speed()
                                      + self.CALORIES_MEAN_SPEED_SHIFT)
                                      * self.weight_kg
                                      / self.M_IN_KM
                                      * self.duration_h
                                      * self.MIN_IN_H)
        return spent_calories_kkal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action_pcs: float,
                 duration_h: float,
                 weight_kg: float,
                 height_cm: float,
                 *args: list
                 ) -> None:
        super().__init__(action_pcs, duration_h, weight_kg)
        self.height_cm: float = height_cm

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        spent_calories_kkal: float = ((self.CALORIES_WEIGHT_MULTIPLIER
                                       * self.weight_kg
                                       + ((self.get_mean_speed()
                                           * self.KMH_IN_MSEC)
                                           ** 2
                                           / (self.height_cm
                                              / self.CM_IN_M))
                                       * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                       * self.weight_kg)
                                      * self.duration_h
                                      * self.MIN_IN_H)
        return spent_calories_kkal


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(self,
                 action_pcs: float,
                 duration_h: float,
                 weight_kg: float,
                 length_pool_m: float,
                 count_pool_pcs: int,
                 *args: list
                 ) -> None:
        super().__init__(action_pcs, duration_h, weight_kg)
        self.length_pool_m: float = length_pool_m
        self.count_pool_pcs: int = count_pool_pcs

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость движения."""
        mean_speed_kmph: float = (self.length_pool_m
                                  * self.count_pool_pcs
                                  / self.M_IN_KM
                                  / self.duration_h)
        return mean_speed_kmph

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        spent_calories_kkal: float = ((self.get_mean_speed()
                                      + self.CALORIES_MEAN_SPEED_SHIFT)
                                      * self.CALORIES_WEIGHT_MULTIPLIER
                                      * self.weight_kg
                                      * self.duration_h)
        return spent_calories_kkal


def read_package(workout_type: str, data: list) -> Training:
    """Читает данные, полученные от датчиков."""
    WORKOUT_CLASSES: dict[str, Type] = {'SWM': Swimming,
                                        'RUN': Running,
                                        'WLK': SportsWalking
                                        }
    if workout_type not in WORKOUT_CLASSES:
        raise Exception('<указанного типа тренировки нет в программе>')
    else:
        workout = WORKOUT_CLASSES[workout_type](*data)
        return workout


def main(training: Training) -> None:
    """Главная функция."""
    info_first: InfoMessage = training.show_training_info()
    info: str = info_first.get_message()
    return print(info)


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [('SWM', [720, 1, 80, 25, 40]),
                                             ('RUN', [15000, 1, 75]),
                                             ('WLK', [9000, 1, 75, 180]),
                                             ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
