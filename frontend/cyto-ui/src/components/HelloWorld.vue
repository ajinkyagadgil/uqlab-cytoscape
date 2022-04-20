<template>
  <div id="hello">
    <div id="cyto" ref="cyto">
      <!-- <button id="draw-on" style="color: red">Draw mode on</button>
    <button id="draw-off" @click="saveData()">Save</button> -->
      <cytoscape
        ref="cyRef"
        :config="config"
        v-on:mousedown="addNodeDetails"
        :preConfig="preConfig"
        :afterCreated="afterCreated"
      >
        <cy-element
          v-for="def in elements"
          :key="`${def.data.id}`"
          :definition="def"
          v-on:cxttap="updateGraphNode(def.data.id)"
        />
        <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col>
                    <v-text-field
                      v-model="nodeDetails.node_name"
                      label="Node Name"
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-select
                      v-model="nodeDetails.nodeType"
                      :items="nodeTypes"
                      item-text="nodeType"
                      item-value="value"
                      label="Select Node Type"
                    ></v-select>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col  v-if="nodeDetails.nodeType==0" >
                    <v-slider v-model="nodeDetails.nodeTypeValue" min="1" max="10" :thumb-color="sliderColor" thumb-label="always" label=""> </v-slider>
                  </v-col>
                  <v-col v-if="nodeDetails.nodeType==1">
                    <v-slider v-model="nodeDetails.nodeTypeValue" min="-9999" max="9999" :thumb-color="sliderColor" thumb-label="always" label=""> </v-slider>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn
                color="blue darken-1"
                v-if="editedIndex != -1"
                text
                @click="deleteItemConfirmDialog"
              >
                Delete
              </v-btn>
              <v-btn color="blue darken-1" text @click="close"> Cancel </v-btn>
              <v-btn color="blue darken-1" text @click="addNode"> Save </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5"
              >Are you sure you want to delete this item?</v-card-title
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete"
                >Cancel</v-btn
              >
              <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                >OK</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </cytoscape>
      <v-btn depressed color="primary" @click="saveAll()"> Save Changes </v-btn>
      <v-row>
        <v-col>
          <v-slider v-model="dataGenerateValue" min="50" max="300" :thumb-color="sliderColor" thumb-label="always" label=""> </v-slider>
        <v-btn depressed color="primary" @click="generateData(dataGenerateValue)"> Generate Data </v-btn>
        </v-col>

      </v-row>
      
    </div>
  </div>
</template>

<script>
import config from "../cyto-config";
// import jquery from "jquery";
// import contextMenus from "cytoscape-context-menus";
import "cytoscape-context-menus/cytoscape-context-menus.css";
import axios from "axios";
import cytoscape from "cytoscape";

// import cytoscape from 'cytoscape';
import edgehandles from "cytoscape-edgehandles";

// const elements = [...config.elements];
const elements = [];
delete config.elements;
export default {
  name: "HelloWorld",
  data() {
    return {
      dialog: false,
      dialogDelete: false,
      config,
      elements,
      isDrawMode: false,
      json1_data: "",
      editedIndex: -1,
      dataGenerateValue: 50,
      nodeDetails: {
        node_name: "",
        x_point: 0,
        y_point: 0,
        nodeType: 0,
        nodeTypeValue:0 
      },
      defaultItem: {
        node_name: "",
        x_point: 0,
        y_point: 0,
        nodeType: 0,
        nodeTypeValue:0 
      },
      sliderColor: "blue",
      cy: null,
      nodeTypes: [
        { nodeType: "Categorical", value: 0 },
        { nodeType: "Numerical", value: 1 },
      ],
    };
  },
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Node" : "Edit Node";
    },
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },
  methods: {
    saveJSON(data, filename){
    if(!data) {
        console.error('No data')
        return;
    }
    if(!filename) filename = 'console.json'

    if(typeof data === "object"){
        data = JSON.stringify(data, undefined, 4)
    }
    var blob = new Blob([data], {type: 'text/json'}),
        e    = document.createEvent('MouseEvents'),
        a    = document.createElement('a')

    a.download = filename
    a.href = window.URL.createObjectURL(blob)
    a.dataset.downloadurl =  ['text/json', a.download, a.href].join(':')
    e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
    a.dispatchEvent(e)
},

    generateData(value){    
      let n = this.elements.filter((x) => x.group == "nodes");
      let e = this.elements.filter((x) => x.group == "edges");
      let graphData = {
        nodes: n,
        edges: e,
      }; 
      axios
      .post('http://localhost:8000/getData?no_samples=' + value, graphData)
      .then(response => {
        console.log(response.data);
        this.saveJSON(response.data, 'genData-' + value + '.json')
        
      })
      .catch(error => {
        console.log(error)
      })
      
    },
    saveAll() {
      let n = this.elements.filter((x) => x.group == "nodes");
      let e = this.elements.filter((x) => x.group == "edges");
      let graphData = {
        nodes: n,
        edges: e,
      };
      const dataToSave = {
        data: {
          data: graphData,
        },
      };
      axios.put(`http://localhost:1337/api/graphs/${this.$route.params.id}`, dataToSave)
        .then((response) => {
          console.log(response);
        });
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.nodeDetails = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.nodeDetails = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    deleteItemConfirmDialog() {
      this.dialogDelete = true;
    },
    deleteItemConfirm() {
      //let elemenToDelete = JSON.stringify(this.elements[this.editedIndex])
      this.elements.forEach(element => {
        //if the type of node is edge and if the source or destination is equal to node to be deleted then delete object
        if(element.group == 'edges' && (element.data.source==this.elements[this.editedIndex].data.id || element.data.target==this.elements[this.editedIndex].data.id)) {
          this.elements.splice(this.elements.indexOf(element), 1);
          console.log(this.$route.params.id)
        }
      })
      this.elements.splice(this.editedIndex, 1);
      this.close();
      this.closeDelete();
    },
    addNode() {
      // console.log("This is cy ref",this.$refs.cyRef.cy)
      console.log("Edited index is", this.editedIndex);
      console.log(this.nodeDetails.nodeType);
      if (this.editedIndex == -1) {
        //add new node {
        const nextNode = {
          data: { id: this.nodeDetails.node_name },
          position: {
            x: this.nodeDetails.x_point,
            y: this.nodeDetails.y_point,
          },
          group: "nodes",
          typeParams: {
            nodeType: this.nodeDetails.nodeType,
            nodeTypeValue: this.nodeDetails.nodeTypeValue
          }
        };
        this.elements = [...this.elements, nextNode];
      } else {
        let element = this.elements[this.editedIndex];
        console.log("The original element is", JSON.stringify(element));
        element.data.id = this.nodeDetails.node_name;
        element.typeParams.nodeType = this.nodeDetails.nodeType;
        element.typeParams.nodeTypeValue = this.nodeDetails.nodeTypeValue;
        console.log("AAfter update", JSON.stringify(this.elements));
      }
      //cy.add(nextNode)

      this.dialog = false;
      console.log(JSON.stringify(this.elements));
    },
    async getGraphData(id) {
      const res = await fetch(`http://localhost:1337/api/graphs/${id}`);
      return res.json();
    },
    addNodeDetails(event) {
      this.nodeDetails = {
        node_name: "",
        x_point: 0,
        y_point: 0,
        nodeType: this.defaultItem.nodeType,
        nodeTypeValue:this.defaultItem.nodeTypeValue
      };
      if (event.target === this.$refs.cyRef.instance) {
        this.nodeDetails.x_point = event.originalEvent.layerX;
        this.nodeDetails.y_point = event.originalEvent.layerY;
        this.nodeDetails.nodeType = this.defaultItem.nodeType;
        this.nodeDetails.nodeTypeValue = this.defaultItem.nodeTypeValue;
        this.dialog = true;
      }
    },
    // saveData() {
    //   const s = this.json1_data;

    //   const dataToSave = {
    //     data: {
    //       Graph_Id: "graph110",
    //       Name: "graph 110",
    //       data: s,
    //     },
    //   };
    //   // console.log(JSON.stringify(data))
    //   axios
    //     .post("http://localhost:1337/api/graphs", dataToSave)
    //     .then((response) => {
    //       console.log(response);
    //     });
    // },
    // saveChanges(cy) {
    //   console.log("The cy in save changes is", cy.json()["elements"]);
    //   console.log(
    //     "JSON data in save changes",
    //     JSON.stringify(cy.json()["elements"])
    //   );
    //   this.json1_data = cy.json()["elements"];
    // },
    updateGraphNode(id) {
      let node = this.elements.find((x) => x.data.id == id);
      this.nodeDetails.node_name = node.data.id;
      this.nodeDetails.x_point = node.position.x;
      this.nodeDetails.y_point = node.position.y;
      this.nodeDetails.nodeType = node.typeParams.nodeType;
      this.nodeDetails.nodeTypeValue = node.typeParams.nodeTypeValue;
      this.editedIndex = this.elements.indexOf(node);
      this.nodeDetails = Object.assign({}, this.nodeDetails);
      this.dialog = true;
    },
    deleteGraphNode(id) {
      let node = this.elements.find((x) => x.data.id == id);
      this.editedIndex = this.elements.indexOf(node);
      this.dialogDelete = true;
      console.log(id);
    },
    deleteNode(id) {
      console.log("node clicked", id);
    },
    updateNode(event) {
      console.log("right click node", event);
    },
    toggleDialog() {
      this.dialog = true;
    },
    preConfig(cytoscape) {
      if (!cytoscape("core", "edgehandles")) {
        //cytoscape.use(cxtmenu);
        //contextMenus(cytoscape, jquery);

        edgehandles(cytoscape);
      }

      // cytoscape.use(edgehandles);
      console.log("calling pre-config", cytoscape);
    },
    afterCreated(cy) {
      console.log("After created called");
      // cy: this is the cytoscape instance
      console.log("after created", cy);
      // cy.contextMenus({
      //   menuItems: [
      //     {
      //       id: "remove",
      //       content: "remove",
      //       tooltipText: "remove",
      //       image: { src: "remove.svg", width: 12, height: 12, x: 6, y: 4 },
      //       selector: "node, edge",
      //       onClickFunction: function (event) {
      //         var target = event.target || event.cyTarget;
      //         console.log(target);
      //         target.remove();
      //       },
      //       hasTrailingDivider: true,
      //     },
      //     {
      //       id: "edit",
      //       content: "edit",
      //       tooltipText: "edit",
      //       selector: "*",
      //       onClickFunction: () => {
      //         //var target = event.target || event.cyTarget;
      //         //target.hide();
      //         console.log("This is edit rc", JSON.stringify(this.elements));
      //       },
      //       disabled: false,
      //     },
      //   ],
      // });
      var eh = cy.edgehandles({
        canConnect: function (sourceNode, targetNode) {
          // whether an edge can be created between source and target
          return !sourceNode.same(targetNode); // e.g. disallow loops
        },
        edgeParams: (sourceNode, targetNode) => {
          console.log(sourceNode.data().id);
          console.log("Soure node is", sourceNode);
          console.log("Dest node is", targetNode);
          // for edges between the specified source and target
          // return element object to be passed to cy.add() for edge

          const newEdge = {
            data: {
              id: sourceNode.data().id + targetNode.data().id,
              source: sourceNode.data().id,
              target: targetNode.data().id,
            },
            group: "edges",
          };

          console.log(newEdge);
          this.elements = [...this.elements, newEdge];
          console.log("After adding edges", JSON.stringify(this.elements));

          //return { group: 'edges', data: { id: sourceNode+targetNode, source: sourceNode, target: targetNode } };
        },

        cxt: true,
        enabled: true,
        hoverDelay: 150, // time spent hovering over a target node before it is considered selected
        snap: true, // when enabled, the edge can be drawn by just moving close to a target node (can be confusing on compound graphs)
        snapThreshold: 50, // the target node must be less than or equal to this many pixels away from the cursor/finger
        snapFrequency: 15, // the number of times per second (Hz) that snap checks done (lower is less expensive)
        noEdgeEventsInDraw: false, // set events:no to edges during draws, prevents mouseouts on compounds
        disableBrowserGestures: true, // during an edge drawing gesture, disable browser gestures such as two-finger trackpad swipe and pinch-to-zoom
      });
      console.log("Draw Mode", this.isDrawMode);
      // console.log("Edge param is",eh.edgeParams)
      // document.querySelector("#draw-on").addEventListener("click", function () {
      //   eh.enableDrawMode();
      // });

      // document
      //   .querySelector("#draw-off")
      //   .addEventListener("click", function () {
      //     eh.disableDrawMode();
      //   });
      // if (this.$toggle) {
      //   eh.enableDrawMode();
      // } else {
      //   eh.disableDrawMode();
      // }
      // if(this.isDrawMode) {
      eh.enableDrawMode();
      console.log("EH is", eh);

      // }
    },
  },
  async created() {
    const { data } = await this.getGraphData(this.$route.params.id);
    console.log("The data is", JSON.stringify(data));
    if (data.attributes.data != null) {
      this.elements = [
        ...data.attributes.data.nodes,
        ...data.attributes.data.edges,
      ];
    }
    //this.elements = [...data[3].attributes.data.nodes, ...data[3].attributes.data.edges];
  },
  mounted() {
    const cy = cytoscape({
      container: this.$refs.cyto,
      // elements: [{data: { id: "a" }}]
    });
    // this.cy = cy;
    this.getCy = () => {
      return cy;
    };
  },
  
};
</script>
<style>
#cyto {
  width: 1170px;
  height: 600px;
  display: block;
  background-color: cornsilk;
}
</style>
