import {
	BarChart,
	XAxis,
	YAxis,
	Tooltip,
	Legend,
	Bar,
	ResponsiveContainer,
	CartesianGrid,
} from 'recharts';

export function BarGraph({
	data,
	XAxisLabel,
	YAxisLabel,
	dataKeys,
	margin,
	minHeight,
	minWidth,
	legend = false,
	tooltip = false,
}) {
	return (
		<ResponsiveContainer width='100%' minHeight={minHeight} minWidth={minWidth}>
			<BarChart data={data} margin={margin}>
				<CartesianGrid strokeDasharray='3 3' />
				<XAxis dataKey={XAxisLabel} />
				<YAxis dataKey={YAxisLabel} />
				{tooltip && <Tooltip />}
				{legend && <Legend />}
				{dataKeys.map((dataKey, index) => (
					<Bar
						dataKey={dataKey.key}
						fill={dataKey.color}
						key={`bar-charts-${index}`}
					/>
				))}
			</BarChart>
		</ResponsiveContainer>
	);
}
