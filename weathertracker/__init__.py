from flask import Flask, request, Response, abort, jsonify
import simplejson
import iso8601
from datetime import timedelta


app = Flask('weathertracker')

measurements = dict()


class WeatherData:
    def __init__(self):
        self.timestamp = None
        self.temperature = None
        self.dewPoint = None
        self.precipitation = None

    def jsonify(self):
        return simplejson.dumps({
            "timestamp": self.timestamp.isoformat().replace('+00:00', '.000Z'),
            "temperature": self.temperature,
            "dewPoint": self.dewPoint,
            "precipitation": self.precipitation
        })

    def validate(self):
        if self.timestamp is None:
            return False
        try:
            self.timestamp = iso8601.parse_date(self.timestamp)
            self.temperature = float(self.temperature)
            self.dewPoint = float(self.dewPoint)
            self.precipitation = float(self.precipitation)
        except:
            return False
        return True


# TODO: Implement the endpoints in the ATs.
# The below stubs are provided as a starting point.
# You may refactor them however you like, so long as a Flask instance is set
# to `app`


not_implemented = 'Not Implemented\n', 501, {'Content-Type': 'text/plain'}

# dummy handler so you can tell if the server is running
# e.g. `curl localhost:8000`


@app.route('/')
def root():
    return 'Weather tracker is up and running!\n'


# features/01-measurements/01-add-measurement.feature
@app.route('/measurements', methods=['POST'])
def create_measurement():
    if not request.json:
        abort(400)
    data = WeatherData()
    data.timestamp = request.json.get('timestamp', None)
    data.temperature = request.json.get('temperature', None)
    data.dewPoint = request.json.get('dewPoint', None)
    data.precipitation = request.json.get('precipitation', None)
    if data.validate():
        measurements[data.timestamp] = data
        response = Response(response=data.jsonify(), status=201)
        response.headers['location'] = '/measurements/' + request.json.get('timestamp')
        return response
    else:
        abort(400)


@app.route('/measurements/<timestamp>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def update_measurement(timestamp):
    # features/01-measurements/02-get-measurement.feature
    if request.method == 'GET':
        print(len(timestamp))
        if not timestamp:
            abort(400)
        if len(timestamp) == 24:
            try:
                format_time = iso8601.parse_date(timestamp)
            except:
                abort(400)
            if format_time in measurements:
                return measurements[format_time].jsonify(), 200
            else:
                abort(404)
        if len(timestamp) == 10:
            try:
                format_time = iso8601.parse_date(timestamp)
            except:
                abort(400)
            oneMoreDay = format_time + timedelta(days=1)
            results = list()
            for key in measurements:
                if format_time < measurements[key].timestamp < oneMoreDay:
                    results.append(measurements[key].jsonify())
            if not results:
                abort(404)
            else:
                return '[' + ', '.join(results) + ']', 200
        else:
            abort(404)



    # features/01-measurements/03-update-measurement.feature
    if request.method == 'PUT':
        if not timestamp:
            abort(400)
        try:
            format_time = iso8601.parse_date(timestamp)
        except:
            abort(400)

        if format_time in measurements:
            if timestamp != request.json.get('timestamp'):
                abort(409)
            if request.json.get('temperature') is None \
                or request.json.get('dewPoint') is None \
                    or request.json.get('precipitation') is None:
                abort(400)
            data = WeatherData()
            data.timestamp = request.json.get('timestamp', None)
            data.temperature = request.json.get('temperature', None)
            data.dewPoint = request.json.get('dewPoint', None)
            data.precipitation = request.json.get('precipitation', None)
            if data.validate():
                measurements[format_time] = data
            else:
                abort(400)
            return "OK", 204
        else:
            abort(404)

    # features/01-measurements/03-update-measurement.feature
    if request.method == 'PATCH':
        if not timestamp:
            abort(400)
        try:
            format_time = iso8601.parse_date(timestamp)
        except:
            abort(400)

        if format_time in measurements:
            if timestamp != request.json.get('timestamp'):
                abort(409)
            data = WeatherData()
            data.timestamp = format_time
            data.temperature = request.json.get('temperature')
            data.dewPoint = request.json.get('dewPoint')
            data.precipitation = request.json.get('precipitation')
            if data.temperature is not None:
                try:
                    measurements[format_time].temperature = float(data.temperature)
                except:
                    abort(400)
            if data.dewPoint is not None:
                try:
                    measurements[format_time].dewPoint = float(data.dewPoint)
                except:
                    abort(400)
            if data.precipitation is not None:
                try:
                    measurements[format_time].precipitation = float(data.precipitation)
                except:
                    abort(400)
            return measurements[format_time].jsonify(), 204
        else:
            abort(404)

    # features/01-measurements/04-delete-measurement.feature
    if request.method == 'DELETE':
        if not timestamp:
            abort(400)
        try:
            format_time = iso8601.parse_date(timestamp)
        except:
            abort(400)

        if format_time in measurements:
            del measurements[format_time]
            return "Record deleted", 204
        else:
            abort(404)


# features/02-stats/01-get-stats.feature
@app.route('/stats')
def stats():
    if request.method == 'GET':
        stats = request.args.getlist('stat')
        metrics = request.args.getlist('metric')
        fromDateTime = iso8601.parse_date(request.args.get('fromDateTime'))
        toDateTime = iso8601.parse_date(request.args.get('toDateTime'))

        results = list()
        dateRange = list()

        for key in measurements:
            if fromDateTime < measurements[key].timestamp < toDateTime:
                dateRange.append(measurements[key])

        for m in metrics:
            for s in stats:
                temp = list()
                for x in dateRange:
                    if m == 'temperature':
                        temp.append(x.temperature)
                    if m == 'dewPoint':
                        temp.append(x.dewPoint)
                    if m == 'precipitation':
                        temp.append(x.precipitation)
                if s == "min":
                    minTemp = round(min(temp), 1)
                    results.append({"metric": m, "stat": s, "value": minTemp})
                if s == "max":
                    maxTemp = round(max(temp), 1)
                    results.append({"metric": m, "stat": s, "value": maxTemp})
                if s == "average":
                    avgTemp = round(sum(temp)/len(temp), 1)
                    results.append({"metric": m, "stat": s, "value": avgTemp})

        return jsonify(results)
