import * as d3 from 'd3'

export default function render ({cells, gridWidth, gridHeight, matrixData, params}) {
  params = params || {}
  let attrs = (params['attribute'] || '').split('.')
  function accesssor (d) {
    for (let attr of attrs) {
      if (d !== undefined) {
        d = d[attr]
      }
    }
    return d
  }

  let marginGridWidth = gridWidth * 0.8
  let marginGridHeight = gridHeight * 0.8

  matrixData.forEach(matrixRow => matrixRow.forEach(arr => {
    let _yMax = d3.max(arr, accesssor) || 0
    let _xMax = arr.length || 0
    let _xScale = d3.scale
      .ordinal()
      .domain(d3.range(_xMax))
      .rangeBands([0, marginGridWidth])

    let _yScale = d3.scale
      .linear()
      .domain([0, _yMax])
      .range([marginGridHeight, 0])

    let _xAxis = d3.svg.axis()
      .scale(_xScale)
      .orient('bottom')

    let _yAxis = d3.svg.axis()
      .scale(_yScale)
      .orient('left')

    Object.assign(arr, {
      _xMax,
      _yMax,
      _xScale,
      _yScale,
      _xAxis,
      _yAxis
    })
  }))

  cells
    .filter(d => d._xMax === 0 || d._yMax === 0)
    .append('text')
    .text('NO DATA')
    .attr('x', gridWidth * 0.5)
    .attr('y', gridHeight * 0.5 + 5)
    .attr('font-size', '20px')
    .attr('fill', d => 'rgb(255,255,255)')
    .style('text-anchor', 'middle')
    .transition()
    .duration(750)
    .ease('linear')
    .attr('fill', 'rgb(255, 130, 130)')

  cells = cells
    .filter(d => d._xMax !== 0 && d._yMax !== 0)
    .append('g')
    .attr('transform', 'translate(' + marginGridWidth * 0.1 + ',' + marginGridHeight * 0.1 + ')')

  cells
    .append('g')
    .each(function (d, i) {
      d3.select(this)
        .call(d._xAxis)
    })
    .attr('transform', 'translate(0,' + marginGridHeight + ')')
    .style('fill', 'none')
    .style('stroke', 'black')
    .style('shape-rendering', 'crispEdges')
    .style('font-size', '11px')

  cells.append('g')
    .each(function (d, i) {
      d3.select(this)
        .call(d._yAxis)
    })
    .style('fill', 'none')
    .style('stroke', 'black')
    .style('shape-rendering', 'crispEdges')
    .style('font-size', '8px')

  cells.selectAll('bar')
    .data(d => d)
    .enter()
    .append('rect')
    .style('fill', 'rgb(255, 255, 255)')
    .attr('height', d => marginGridHeight - d._arr._yScale(accesssor(d)))
    .attr('width', d => (marginGridWidth * 0.8) / d._arr._xMax)
    .attr('x', (d, i) => d._arr._xScale(i))
    .attr('y', (d, i) => d._arr._yScale(accesssor(d)))
    .attr('transform', 'translate(' + marginGridWidth * 0.05 + ',0)')
    .transition()
    .duration(1000)
    .ease('linear')
    .style('fill', 'rgb(158, 178, 248)')
}
