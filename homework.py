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
                 action: float,
                 duration: float,
                 weight: float,
                 *args: list
                 ) -> None:
        # Получает данные в ед.изм "шт.":
        self.action: float = action
        # Получает данные в ед.изм "ч.":
        self.duration: float = duration
        # Получает данные в ед.изм "кг":
        self.weight: float = weight

    def get_distance(self) -> float:
        """Возвращает дистанцию в км."""
        distance_km: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость движения."""
        distance: float = self.get_distance()
        mean_speed: float = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training: InfoMessage = InfoMessage(type(self).__name__,
                                            self.duration,
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
                                      * self.weight
                                      / self.M_IN_KM
                                      * self.duration
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
                 action: float,
                 duration: float,
                 weight: float,
                 height: float,
                 *args: list
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        spent_calories_kkal: float = ((self.CALORIES_WEIGHT_MULTIPLIER
                                       * self.weight
                                       + ((self.get_mean_speed()
                                           * self.KMH_IN_MSEC)
                                           ** 2
                                           / (self.height
                                              / self.CM_IN_M))
                                       * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                       * self.weight)
                                      * self.duration
                                      * self.MIN_IN_H)
        return spent_calories_kkal


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 *args: list
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость движения."""
        mean_speed: float = (self.length_pool
                                  * self.count_pool
                                  / self.M_IN_KM
                                  / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        spent_calories: float = ((self.get_mean_speed()
                                      + self.CALORIES_MEAN_SPEED_SHIFT)
                                      * self.CALORIES_WEIGHT_MULTIPLIER
                                      * self.weight
                                      * self.duration)
        return spent_calories


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
