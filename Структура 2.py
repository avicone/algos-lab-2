class BusStop:
    def __init__(self, name, x, y, time_to_next=0):
        self.name = name
        self.x = x 
        self.y = y  
        self.time_to_next = time_to_next 


class BusRoute:
    def __init__(self):
        self.stops = []
    
    def add_stop(self, name, x, y, time_to_next=0):
        stop = BusStop(name, x, y, time_to_next)
        self.stops.append(stop)
        print(f"Остановка '{name}' добавлена")
    
    def total_time(self):
        total = 0
        for stop in self.stops:
            total += stop.time_to_next
        return total
    
    def bus_place(self, n_stops, start_index=0):
        if not self.stops:
            return "Маршрут пуст"
        
        if start_index < 0 or start_index >= len(self.stops):
            return "Неверный индекс начальной остановки"
        
        if len(self.stops) == 1:
            return self.stops[0].name
        current_index = start_index
        direction = 1
        for i in range(n_stops):
            current_index += direction
            
            if current_index >= len(self.stops):
                current_index = len(self.stops) - 2 
                direction = -1
            elif current_index < 0:
                current_index = 1
                direction = 1
        
        return self.stops[current_index].name
    
    def arrival_time(self, n_stops, start_index=0):
        if not self.stops:
            return "Маршрут пуст"
        
        if start_index < 0 or start_index >= len(self.stops):
            return "Неверный индекс начальной остановки"
        
        if len(self.stops) == 1:
            return "0 мин"
        
        total_minutes = 0
        current_index = start_index
        direction = 1  
        for i in range(n_stops):
            if direction == 1: 
                total_minutes += self.stops[current_index].time_to_next
            else: 
                total_minutes += self.stops[current_index - 1].time_to_next
            
            current_index += direction
            if current_index >= len(self.stops):
                current_index = len(self.stops) - 2  
                direction = -1
            elif current_index < 0:
                current_index = 1  
                direction = 1
        
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours > 0:
            return f"{hours} ч {minutes} мин"
        else:
            return f"{minutes} мин"
    
    def homeway(self):
        way_home = BusRoute()
        for i in range(len(self.stops) - 1, -1, -1):
            stop = self.stops[i]
            if i > 0:
                time_to_next = self.stops[i-1].time_to_next
            else:
                time_to_next = 0
            way_home.add_stop(stop.name, stop.x, stop.y, time_to_next)
        
        return way_home
    
    def print_route(self):
        if not self.stops:
            print("Маршрут пуст")
            return
        print("\n" + "="*70)
        print(f"{'№':<4} {'Название':<20} {'Координаты':<15} {'Время до след.':<15} {'Время от начала':<15}")
        print("="*70)
        cumulative_time = 0
        for i, stop in enumerate(self.stops):
            coords = f"({stop.x}, {stop.y})"
            time_str = f"{stop.time_to_next} мин" if stop.time_to_next > 0 else "-"
            cum_time_str = f"{cumulative_time} мин"
            print(f"{i+1:<4} {stop.name:<20} {coords:<15} {time_str:<15} {cum_time_str:<15}")
            cumulative_time += stop.time_to_next
        
        print("="*70)
        print(f"Общее время маршрута в одну сторону: {self.total_time()} мин")
    
    def get_stop_names(self):
        """Получить список названий остановок"""
        return [stop.name for stop in self.stops]
    
    def show_stops_list(self):
        if not self.stops:
            print("Маршрут пуст")
            return False
        
        print("\nСписок остановок:")
        print("-" * 40)
        for i, stop in enumerate(self.stops):
            print(f"{i+1}. {stop.name}")
        print("-" * 40)
        return True


def input_stop():
    print("\n--- Добавление новой остановки ---")
    name = input("Введите название остановки: ")
    
    while True:
        try:
            x = float(input("Введите координату X: "))
            break
        except ValueError:
            print("Ошибка! Введите число для координаты X.")
    
    while True:
        try:
            y = float(input("Введите координату Y: "))
            break
        except ValueError:
            print("Ошибка! Введите число для координаты Y.")
    
    while True:
        try:
            time_to_next = input("Введите время до следующей остановки (в минутах, для последней остановки - 0): ")
            if time_to_next == "":
                time_to_next = 0
            else:
                time_to_next = float(time_to_next)
            if time_to_next < 0:
                print("Время не может быть отрицательным!")
                continue
            break
        except ValueError:
            print("Ошибка! Введите число.")
    
    return name, x, y, time_to_next


def choose_start_stop(route):
    if not route.show_stops_list():
        return None
    
    while True:
        try:
            choice = input(f"Выберите номер остановки (1-{len(route.stops)}): ")
            if choice == "":
                print("Будет использована первая остановка (№1)")
                return 0
            start_num = int(choice) - 1
            if 0 <= start_num < len(route.stops):
                print(f"Выбрана остановка: {route.stops[start_num].name}")
                return start_num
            else:
                print(f"Ошибка! Введите число от 1 до {len(route.stops)}")
        except ValueError:
            print("Ошибка! Введите целое число.")


def main():
    print("Система управления автобусным маршрутом")
    print("-" * 40)
    
    route = BusRoute()
    
    while True:
        
        print("\n" + "="*50)
        print("МЕНЮ:")
        print("1. Добавить остановку")
        print("2. Показать маршрут")
        print("3. Узнать, где будет автобус через N остановок")
        print("4. Узнать время прибытия через N остановок")
        print("5. Показать обратный маршрут")
        print("6. Очистить маршрут")
        print("0. Выход")
        print("="*50)
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            name, x, y, time_to_next = input_stop()
            route.add_stop(name, x, y, time_to_next)
            
        elif choice == "2":
            if not route.stops:
                print("Сначала добавьте остановки в маршрут!")
                continue
            print("\nТекущий маршрут:")
            route.print_route()
            
        elif choice == "3":
            if not route.stops:
                print("Сначала добавьте остановки в маршрут!")
                continue
            
            print("\nОт какой остановки считать?")
            start_index = choose_start_stop(route)
            if start_index is None:
                continue
                
            while True:
                try:
                    n = int(input("Через сколько остановок узнать место? "))
                    if n < 0:
                        print("Введите неотрицательное число!")
                        continue
                    break
                except ValueError:
                    print("Ошибка! Введите целое число.")
            
            start_name = route.stops[start_index].name
            result = route.bus_place(n, start_index)
            print(f"\nАвтобус от остановки '{start_name}' через {n} остановок будет на: {result}")
            
        elif choice == "4":
            if not route.stops:
                print("Сначала добавьте остановки в маршрут!")
                continue
            
            print("\nОт какой остановки считать время?")
            start_index = choose_start_stop(route)
            if start_index is None:
                continue
                
            while True:
                try:
                    n = int(input("Через сколько остановок узнать время прибытия? "))
                    if n < 0:
                        print("Введите неотрицательное число!")
                        continue
                    break
                except ValueError:
                    print("Ошибка! Введите целое число.")
            
            start_name = route.stops[start_index].name
            result = route.arrival_time(n, start_index)
            print(f"\n Время прибытия от остановки '{start_name}' через {n} остановок: {result}")
            
        elif choice == "5":
            if not route.stops:
                print("Сначала добавьте остановки в маршрут!")
                continue
                
            print("\nОбратный маршрут:")
            homeway = route.homeway()
            homeway.print_route()
            
        elif choice == "6":
            route = BusRoute()
            print("Маршрут очищен!")

        elif choice == "0":
            print("До свидания!")
            break
            
        else:
            print("Неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    main()
