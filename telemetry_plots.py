from telemetry_plot import TelemetryPlot

class TelemetryPlots:
    def __init__(self):
        self.x_vel = TelemetryPlot('x velocity',row=0,col=0,tick_increment=3)
        self.y_vel = TelemetryPlot('y velocity',row=0,col=1,tick_increment=3)
        self.robot_angle = TelemetryPlot('robot angle',row=1,col=0,tick_increment=40)
        self.angle_error = TelemetryPlot('angle error',row=1,col=1,tick_increment=40)
        self.plots = [self.x_vel, self.y_vel, self.robot_angle, self.angle_error]

    def render_init(self, screen):
        for plot in self.plots:
            plot.render_init(screen)

    def render(self, screen):
        for plot in self.plots:
            plot.erase_update_render(screen)
