from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_MESSAGE_TXT = ('Тип тренировки: {training_type}; '
                        'Длительность: {duration:.3f} ч.; '
                        'Дистанция: {distance:.3f} км; '
                        'Ср. скорость: {speed:.3f} км/ч; '
                        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.INFO_MESSAGE_TXT.format(training_type=self.training_type,
                                            duration=self.duration,
                                            distance=self.distance,
                                            speed=self.speed,
                                            calories=self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration_h
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration_h,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_RUNNING_CALORIE_1: int = 18
    COEFF_RUNNING_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.COEFF_RUNNING_CALORIE_1 * self.get_mean_speed()
                    - self.COEFF_RUNNING_CALORIE_2)
                    * self.weight / self.M_IN_KM
                    * self.duration_h * self.MIN_IN_HOUR)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_SPORTS_WALKING_CALORIE_1: float = 0.035
    COEFF_SPORTS_WALKING_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.COEFF_SPORTS_WALKING_CALORIE_1 * self.weight
                    + (self.get_mean_speed()**2 // self.height)
                    * self.COEFF_SPORTS_WALKING_CALORIE_2
                    * self.weight)
                    * self.duration_h * self.MIN_IN_HOUR)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_SWIM_CALORIE_1: float = 1.1
    COEFF_SWIM_CALORIE_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.length_pool
                 * self.count_pool
                 / self.M_IN_KM
                 / self.duration_h)
        return speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed()
                    + self.COEFF_SWIM_CALORIE_1)
                    * self.COEFF_SWIM_CALORIE_2
                    * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}

    if workout_type in workout_types:
        class_name = workout_types[workout_type]
        return class_name(*data)
    else:
        raise ValueError(f'Unknown workout_type {workout_type}!')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
