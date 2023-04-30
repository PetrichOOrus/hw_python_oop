class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.speed = speed
        self.distance = distance
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; Дистанция: '
                f'{self.distance:.3f} км; Ср. скорость: '
                f'{self.speed:.3f} км/ч; Потрачено ккал: '
                f'{self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINUTE: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        time_in_minutes = self.duration * self.MINUTE
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * super().get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * time_in_minutes)


class SportsWalking(Training):
    HEIGHT_M = 100
    COEFF_1: float = 0.035
    COEFF_2: float = 0.029
    KM_CONST = 0.278
    """Тренировка: спортивная ходьба."""
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        speed_ms = self.get_mean_speed() * self.KM_CONST
        height_in_m = self.height / self.HEIGHT_M
        minutes_training = self.duration * self.MINUTE
        return ((self.COEFF_1 * self.weight
                 + (speed_ms**2 / height_in_m)
                 * self.COEFF_2 * self.weight)
                * minutes_training)


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_3: float = 1.1
    COEFF_4: int = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.COEFF_3) * self.COEFF_4
                * self.weight * self.duration)


workout_types: dict[str, Training] = {'SWM': Swimming,
                                      'RUN': Running,
                                      'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in workout_types:
        return workout_types[workout_type](*data)
    return False


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return info.get_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        print(main(training))
