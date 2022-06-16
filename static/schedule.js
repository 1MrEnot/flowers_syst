const moistureColor = 'rgb(38,119,245)';
const forecastColor = 'rgb(105,162,248)';
const minColor = 'rgba(253,54,99, 0.5)';
const tension = 0.3;

const charts = {};
const userId = getCookie('user_id');

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2)
        return parts.pop().split(';').shift();
}

function drawAllPlots(userInfo){
    userInfo.plants.map(p => p.p_id).forEach(drawPlotById);
}

function drawPlotById(plot_id){
    fetch(`/api/plots/${plot_id}`)
        .then(resp => resp.json())
        .then(res => {
            const id = `g_${res.p_id}`;
            const measurements = res.measurements.map(mapMeasurement);
            const forecast = res.forecast.map(mapMeasurement);
            createChart(id, measurements, forecast, res.min_moisture);
        });
}

const horizontalLinePlugin = {
    id: 'horizontalLine',
    afterDraw: (chartInstance) => {
        const lines = chartInstance.config.options.horizontalLine;
        if (!lines)
            return;

        const yScale = chartInstance.scales["y"];
        const xScale = chartInstance.scales["x"];
        const ctx = chartInstance.ctx;
        const canvas = chartInstance.canvas;

        lines.forEach(line => {
            const style = line.style || "rgba(169,169,169, .6)";
            const yValue = yScale.getPixelForValue(line.y);
            const xValue = xScale.getPixelForValue(0);
            ctx.lineWidth = 3;

            console.log(yValue, yScale.bottom);
            if (yValue >= yScale.bottom)
                return;

            if (yValue) {
                ctx.beginPath();
                ctx.moveTo(xValue, yValue);
                ctx.lineTo(canvas.width, yValue);
                ctx.strokeStyle = style;
                ctx.stroke();
            }

            if (line.text) {
                ctx.fillStyle = style;
                ctx.fillText(line.text, xValue, yValue-10);
                console.log(yValue);
            }
        });
    }
};
Chart.register(horizontalLinePlugin);

function createChart(elementId, measurements, forecast, minValue) {
    const canvas = document.getElementById(elementId);
    const data = {
        datasets: [
            {
                label: 'Влажность',
                backgroundColor: moistureColor,
                borderColor: moistureColor,
                tension: tension,
                data: measurements,
            }
        ]
    };

    if (forecast) {
        data.datasets.push({
            label: 'Прогноз',
            backgroundColor: forecastColor,
            borderColor: forecastColor,
            tension: tension,
            borderDash: [5, 5],
            data: forecast
        });
    }

    const options = {};
    if (minValue){
        options.horizontalLine = [{
            y: minValue,
            style: minColor,
            text: "MIN"
        }];
    }

    const config = {
        type: 'line',
        data: data,
        options: options
    };

    charts[elementId] = new Chart(canvas, config);
}

mapMeasurement = (m) => {
    return {
        x: new Date(m.timestamp).toLocaleString(),
        y: Number(m.value),
    };
}

fetch(`/api/user/${userId}`)
    .then(resp => resp.json())
    .then(drawAllPlots);
