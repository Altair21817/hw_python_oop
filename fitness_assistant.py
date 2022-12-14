"""
Программа фитнесс-ассистента.
Разработана Altair21817.
Все права не защищены.
"""

from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возвращает Информационное сообщение."""

        message: str = ('Тип тренировки: {training_type}; '
                        'Длительность: {duration:.3f} ч.; '
                        'Дистанция: {distance:.3f} км; '
                        'Ср. скорость: {speed:.3f} км/ч; '
                        'Потрачено ккал: {calories:.3f}.')
        return message.format(**asdict(self))


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
        self.action: float = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Возвращает дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

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


WORKOUT_CLASSES: dict[str, type[Training]] = {'SWM': Swimming,
                                              'RUN': Running,
                                              'WLK': SportsWalking
                                              }


def read_package(workout_type: str, data: list) -> Training:
    """Читает данные, полученные от датчиков."""
    return WORKOUT_CLASSES[workout_type](*data)


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
        if workout_type not in WORKOUT_CLASSES:
            print(f'<указанного типа тренировки "{workout_type}" '
                  f'нет в программе>')
        else:
            training: Training = read_package(workout_type, data)
            main(training)
