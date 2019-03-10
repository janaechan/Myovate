graph_data = []


def get_data(arduino):
        while arduino.record:
            data = arduino.get_data()
            if len(graph_data) >= 100:
                graph_data = []
            graph_data.append(data)