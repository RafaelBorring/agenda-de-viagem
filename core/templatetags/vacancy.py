from calendar import LocaleHTMLCalendar
from django import template
from datetime import date
from itertools import groupby
from core.models import List, Holiday, CarType


register = template.Library()


class EventCalendarNode(template.Node):

    def __init__(self, year, month, event_list):
        self.year = template.Variable(year)
        self.month = template.Variable(month)
        self.event_list = template.Variable(event_list)

    def render(self, context):
        my_event_list = self.event_list.resolve(context)
        my_year = self.year.resolve(context)
        my_month = self.month.resolve(context)
        cal = EventCalendar(my_event_list)
        return cal.formatmonth(int(my_year), int(my_month))


class EventCalendar(LocaleHTMLCalendar):

    def __init__(self, events):
        super(EventCalendar, self).__init__(6, 'pt_BR.UTF-8')
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        cars = ''
        for car in CarType.objects.all():
            counter = 0
            for n in List.objects.filter(date__year=self.year, date__month=self.month, date__day=day, car=car):
                counter += n.companion + 1
            if counter > 0:
                cars += '<p>{} <span>{:02d}</span></p>'.format(car, int(car.vacancy - counter))
        dias = range(0, 5)
        feriados = Holiday.objects.filter(date__year=self.year, date__month=self.month, date__day=day)
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events and weekday in dias or feriados and weekday in dias:
                if feriados:
                    cssclass += ' filledzero'
                else:
                    cssclass += ' filled'
                if feriados:
                    return self.day_cell(
                        cssclass,
                        '<span class="dayNumberNoEvents">{}{}</span>'.format(day, cars))
                else:
                    return self.day_cell(
                        cssclass,
                        '<span class="dayNumberNoEvents">{}{}</span>'.format(day, cars))
            if weekday in dias:
                return self.day_cell(
                    cssclass,
                    '<span class="dayNumberNoEvents">{}{}</span>'.format(day, cars))
            return self.day_cell(
                cssclass, '<span class="dayNumberNoEvents">%d</span>' % day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        def field(event): return event.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


@register.tag
def event_calendar(parser, token):
    tag_name, year, month, event_list = token.split_contents()
    return EventCalendarNode(year, month, event_list)
