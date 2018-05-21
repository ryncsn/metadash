<template>
  <v-layout row wrap>
    <v-flex xs12>
      <v-card>
        <v-card-text>
          <v-form v-model="readyToRender">
            <v-container fluid>
              <v-layout row wrap>
                <v-flex xs12 class="px-4">
                  <h4>Entity Filter</h4>
                  <v-divider class="my-3"> </v-divider>
                  <v-flex xs12>
                    <v-select
                      v-model="targetEntity"
                      :items="avaliableEntityNames"
                      :rules="[v => !!v || 'Item is required']"
                      label="Choose an entity to visualize"
                      required
                      ></v-select>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field
                      type="number"
                      label="Entity Limit, How many entity to be loaded for statistic"
                      v-model="entityLimit"
                      :rules="[v => !!v || 'Item is required']"
                      required
                      ></v-text-field>
                  </v-flex>
                </v-flex>
                <v-flex xs12 md6 class="px-4">
                  <v-layout wrap>
                    <v-flex xs12>
                      <h4>Matrix Cordinates</h4>
                      <v-divider class="my-3"> </v-divider>
                    </v-flex>
                    <v-flex xs12>
                      <v-select
                        v-model="xAttribute"
                        :items="avaliableAttributes"
                        :rules="[v => !!v || 'Item is required']"
                        label="X Attribute"
                        required
                        ></v-select>
                    </v-flex>
                    <v-flex xs12>
                      <v-select
                        v-model="yAttribute"
                        :items="avaliableAttributes"
                        :rules="[v => !!v || 'Item is required']"
                        label="Y Attribute"
                        required
                        ></v-select>
                    </v-flex>
                    <v-flex xs12>
                      <v-select
                        v-model="cellAggregator"
                        :items="avaliableAggregatorNames"
                        :rules="[v => !!v || 'Item is required']"
                        label="Cell Aggregator"
                        required
                        ></v-select>
                    </v-flex>
                  </v-layout>
                </v-flex>
                <v-flex xs12 md6 class="px-4">
                  <v-layout wrap>
                    <v-flex xs12>
                      <h4>Aggregator Parameters</h4>
                      <v-divider class="my-3"> </v-divider>
                    </v-flex>
                    <v-flex xs5>
                      <v-text-field
                        type="number"
                        label="Grid Height"
                        v-model="gridHeight"
                        :rules="[v => !!v || 'Item is required']"
                        required
                        ></v-text-field>
                    </v-flex>
                    <v-spacer>
                    </v-spacer>
                    <v-flex xs5>
                      <v-text-field
                        type="number"
                        label="Grid Width"
                        v-model="gridWidth"
                        :rules="[v => !!v || 'Item is required']"
                        required
                        ></v-text-field>
                    </v-flex>
                    <div v-for="aggregatorParam in aggregatorParams">
                      <v-flex xs12>
                        <v-text-field
                          :type="aggregatorParam.type"
                          :label="aggregatorParam.label"
                          v-model="aggregatorParam.value"
                          :rules="[v => !!v || 'Item is required']"
                          required
                          ></v-text-field>
                      </v-flex>
                    </div>
                  </v-layout>
                </v-flex>
                <v-flex xs12 class="px-5">
                  <v-btn block color="primary" @click.native="render" :disabled="!readyToRender">Render</v-btn>
                </v-flex>
              </v-layout>
            </v-container>
          </v-form>
        </v-card-text>
      </v-card>
      <v-flex xs12 class='my-3' v-show='rendered'>
        <v-card>
          <v-card-text>
            <div id='render-zone'>
            </div>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-flex>
  </v-layout>
</template>

<script>
import * as d3 from 'd3'
import heatAggregator from './aggregators/heat'
import barChartAggregator from './aggregators/barChart'
import _ from 'lodash'

var svg = null

export default {
  name: 'matrix-visulizer',
  data () {
    return {
      // Render
      readyToRender: false,
      rendering: false,
      rendered: false,

      // Arguments
      gridHeight: 100,
      gridWidth: 160,
      entityLimit: 100,
      avaliableEntities: {},
      avaliableAttributes: [],
      avaliableAggregators: {
        heatAggregator,
        barChartAggregator
      },
      avaliableAggregatorParams: {
        heatAggregator: [],
        barChartAggregator: [
          {
            'name': 'attribute',
            'type': 'text',
            'label': 'Attributes to be used for bar chart (eg. results.PASSED)',
            'value': ''
          }
        ]
      },

      targetEntity: null,
      cellAggregator: null,
      aggregatorParams: [],
      xAttribute: null,
      yAttribute: null,

      // Data
      data: null
    }
  },
  computed: {
    avaliableEntityNames () {
      return Object.keys(this.avaliableEntities)
    },
    avaliableAggregatorNames () {
      return Object.keys(this.avaliableAggregators)
    }
  },
  watch: {
    cellAggregator (newAggregator) {
      this.aggregatorParams = this.avaliableAggregatorParams[newAggregator]
    },
    targetEntity (newTarget) {
      this.avaliableAttributes = this.avaliableEntities[newTarget].properties
      this.xAttribute = null
      this.yAttribute = null
      this.getData()
    },
    entityLimit () {
      this.getData()
    }
  },
  methods: {
    getData () {
      return this.$mdAPI.get('/matrix-visualizer/' + this.targetEntity + '/?limit=' + this.entityLimit)
        .then(res => res.json())
        .then(data => {
          this.data = data['data']
        })
    },
    refresh () {
      return this.$mdAPI.get('/matrix-visualizer')
        .then(res => res.json())
        .then(data => {
          this.avaliableEntities = data
        })
    },
    render () {
      if (this.rendering) {
        return
      }
      this.rendering = true
      if (svg !== null) {
        svg
          .select('g')
          .remove()
        this.renderer()
      } else {
        svg = d3
          .select('#render-zone')
          .append('svg')
        this.renderer()
      }
      this.rendered = true
      this.rendering = false
    },
    renderer () {
      let data = this.data
      let gridHeight = this.gridHeight
      let gridWidth = this.gridWidth
      let aggregator = this.avaliableAggregators[this.cellAggregator]
      let margin = {top: gridHeight, right: gridWidth, bottom: gridHeight, left: gridWidth}
      let rows = Array.from(data.reduce((set, entity) => set.add(entity['properties'][this.yAttribute]), new Set()))
      let cols = Array.from(data.reduce((set, entity) => set.add(entity['properties'][this.xAttribute]), new Set()))
      let width = gridWidth * cols.length
      let height = gridHeight * rows.length
      let maxLen = 0

      rows.sort()
      cols.sort()

      let matrixDict = {}
      for (const row of rows) {
        let rowDict = {}
        for (const col of cols) {
          rowDict[col] = []
        }
        matrixDict[row] = rowDict
      }

      data.forEach((entity) => {
        let arr = matrixDict[entity['properties'][this.yAttribute]][entity['properties'][this.xAttribute]]
        entity._arr = arr
        arr.push(entity)
        maxLen = arr.length > maxLen ? arr.length : maxLen
      })

      let matrixArr = []
      for (const row of rows) {
        let rowArr = []
        for (const col of cols) {
          rowArr.push(matrixDict[row][col])
        }
        matrixArr.push(rowArr)
      }

      svg
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)

      let g = svg
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

      g.append('rect')
        .fill('red')

      g.selectAll('yLabel')
        .data(rows)
        .enter().append('text')
        .text((d) => _.upperFirst(d))
        .attr('x', 0)
        .attr('y', (d, i) => gridHeight * (i + 0.5))
        .style('text-anchor', 'end')
        .attr('transform', 'translate(-' + margin.left * 0.2 + ', 0)')

      g.selectAll('xLabel')
        .data(cols)
        .enter().append('text')
        .text((d) => _.upperFirst(d))
        .attr('y', 0)
        .attr('x', (d, i) => gridWidth * (i + 0.5))
        .style('text-anchor', 'middle')
        .attr('transform', 'translate(0,-' + margin.top * 0.2 + ')')

      let cellRow = g.selectAll('cell-row')
        .data(matrixArr)
        .enter().append('g')
        .attr('transform', (d, i) => 'translate(0,' + gridHeight * i + ')')

      let cells = cellRow.selectAll('cell')
        .data(d => d)
        .enter().append('g')
        .attr('transform', (d, i) => 'translate(' + gridWidth * i + ', 0)')

      aggregator({
        cells,
        gridWidth,
        gridHeight,
        matrixData: matrixArr,
        params: this.aggregatorParams.reduce(
          (params, param) => {
            params[param.name] = param.value
            return params
          }, {})
      })
    }
  },
  mounted () {
    this.refresh()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  text-align: center;
}

h1, h2 {
  font-weight: normal;
}
.axis path,
.axis line {
    fill: none;
    stroke: black;
    shape-rendering: crispEdges;
}

.axis text {
    font-family: sans-serif;
    font-size: 11px;
}
</style>
