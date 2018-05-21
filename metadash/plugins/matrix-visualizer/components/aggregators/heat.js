import * as d3 from 'd3'

export default function render ({cells, gridWidth, gridHeight, matrixData, params}) {
  let maxLen = 0
  matrixData.forEach(row => {
    row.forEach(entityList => {
      maxLen = entityList.length > maxLen ? entityList.length : maxLen
    })
  })

  let colorScaleR = d3.scale.linear()
    .domain([0, maxLen])
    .rangeRound([255, 0])

  let colorScaleG = d3.scale.linear()
    .domain([0, maxLen])
    .rangeRound([255, 80])

  let colorScaleB = d3.scale.linear()
    .domain([0, maxLen])
    .rangeRound([255, 0])

  cells.append('rect')
    .attr('x', gridWidth * 0.1)
    .attr('y', gridHeight * 0.1)
    .attr('height', gridHeight * 0.8)
    .attr('width', gridWidth * 0.8)
    .style('fill', 'rgb(255,255,255)')
    .transition()
    .duration(750)
    .ease('linear')
    .style('fill', d => 'rgb(' + colorScaleR(d.length) + ', ' + colorScaleG(d.length) + ', ' + colorScaleB(d.length) + ')')

  cells.append('text')
    .text((d, i) => {
      return '' + d.length
    })
    .attr('x', gridWidth * 0.5)
    .attr('y', gridHeight * 0.5 + 5)
    .attr('font-size', '20px')
    .attr('fill', d => 'rgb(255,255,255)')
    .style('text-anchor', 'middle')
    .transition()
    .duration(750)
    .ease('linear')
    .attr('fill', d => 'rgb(' + colorScaleR(d.length) * 2 + ', ' + colorScaleG(d.length) * 2 + ', ' + colorScaleB(d.length) * 2 + ')')
}
