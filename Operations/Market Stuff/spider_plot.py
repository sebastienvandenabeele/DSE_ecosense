import plotly.offline as pyo
import plotly.graph_objects as go

categories = ['Sustainability', 'Scalability',
              'Location Accessibility', 'Reliability', 'Detection Time']
categories = [*categories, categories[0]]

environmental_sensors = [2.6, 2.3, 2.1, 2.8, 2.75]
radiation_sensors = [2.8, 2.5, 2.15, 2.7, 2.7]
aircraft_inspection = [2.2, 2.7, 2.8, 2.65, 2.1]
satellites = [2.45, 2.8, 2.8, 2.1, 2.7]
ecosense = [2.8, 2.6, 2.8, 2.8, 2.75]
environmental_sensors = [*environmental_sensors, environmental_sensors[0]]
radiation_sensors = [*radiation_sensors, radiation_sensors[0]]
aircraft_inspection = [*aircraft_inspection, aircraft_inspection[0]]
satellites = [*satellites, satellites[0]]
ecosense = [*ecosense, ecosense[0]]


fig = go.Figure(
    data=[
        go.Scatterpolar(r=environmental_sensors, theta=categories,
                        name='Environmental Sensors', line={'color': 'red'}),
        go.Scatterpolar(r=radiation_sensors, theta=categories,
                        name='Radiation Sensors', line={'color': 'orange'}),
        go.Scatterpolar(r=aircraft_inspection, theta=categories,
                        name='Visual Inspection by Aircraft', line={'color': 'grey'}),
        go.Scatterpolar(r=satellites, theta=categories,
                        name='Satellite Inspection', line={'color': 'darkturquoise'}),
        go.Scatterpolar(r=ecosense, theta=categories,
                        name='EcoSense EMBER', line={'dash': 'dash', 'color': 'limegreen', 'width': 5})
    ],
    layout=go.Layout(
        title=go.layout.Title(text='Current Wildfire Detection Solutions'),
        polar={'radialaxis': {'visible': True},
               'angularaxis': {'tickfont': {'size': 20}}},
        showlegend=True
    )
)

pyo.plot(fig)
