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
                    <v-checkbox
                      v-model="nodeDetails.selected"
                      label="Selected"
                    ></v-checkbox>
                  </v-col>
                  <v-col>
                    <v-checkbox
                      v-model="nodeDetails.selectable"
                      label="Selectable"
                    ></v-checkbox>
                  </v-col>
                  <v-col>
                    <v-checkbox
                      v-model="nodeDetails.locked"
                      label="Locked"
                    ></v-checkbox>
                  </v-col>
                  <v-col>
                    <v-checkbox
                      v-model="nodeDetails.grabbable"
                      label="Grabbable"
                    ></v-checkbox>
                  </v-col>
                  <v-col>
                    <v-checkbox
                      v-model="nodeDetails.pannable"
                      label="Pannable"
                    ></v-checkbox>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              
              <v-btn color="blue darken-1" v-if="editedIndex != -1" text @click="deleteItemConfirm"> Delete </v-btn>
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
    </div>
  </div>
  <!-- <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/logo.svg')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to Vuetify
        </h1>

        <p class="subheading font-weight-regular">
          For help and collaboration with other Vuetify developers,
          <br>please join our online
          <a
            href="https://community.vuetifyjs.com"
            target="_blank"
          >Discord Community</a>
        </p>
      </v-col>

      <v-col
        class="mb-5"
        cols="12"
      >
        <h2 class="headline font-weight-bold mb-3">
          What's next?
        </h2>

        <v-row justify="center">
          <a
            v-for="(next, i) in whatsNext"
            :key="i"
            :href="next.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ next.text }}
          </a>
        </v-row>
      </v-col>

      <v-col
        class="mb-5"
        cols="12"
      >
        <h2 class="headline font-weight-bold mb-3">
          Important Links
        </h2>

        <v-row justify="center">
          <a
            v-for="(link, i) in importantLinks"
            :key="i"
            :href="link.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ link.text }}
          </a>
        </v-row>
      </v-col>

      <v-col
        class="mb-5"
        cols="12"
      >
        <h2 class="headline font-weight-bold mb-3">
          Ecosystem
        </h2>

        <v-row justify="center">
          <a
            v-for="(eco, i) in ecosystem"
            :key="i"
            :href="eco.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ eco.text }}
          </a>
        </v-row>
      </v-col>
    </v-row>
  </v-container> -->
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
      nodeDetails: {
        node_name: "",
        x_point: 0,
        y_point: 0,
        selected: false,
        selectable: false,
        locked: false,
        grabbable: true,
        pannable: true,
      },
      defaultItem: {
        node_name: "",
        x_point: 0,
        y_point: 0,
        selected: false,
        selectable: false,
        locked: false,
        grabbable: true,
        pannable: true,
      },
      cy: null,
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
    saveAll() {
      let n = this.elements.filter((x) => x.group == "nodes");
      let e = this.elements.filter((x) => x.group == "edges");
      console.log("The nodes are", JSON.stringify(n));
      console.log("The edges are", JSON.stringify(e));
      console.log("Final Changes are", JSON.stringify(this.elements));
      let graphData = {
        nodes: n,
        edges: e,
      };
      console.log("Final data to be saved is", JSON.stringify(graphData));
      const dataToSave = {
        data: {
          data: graphData,
        },
      };
      axios
        .put(
          `http://localhost:1337/api/graphs/${this.$route.params.id}`,
          dataToSave
        )
        .then((response) => {
          console.log(response);
        });
    },

    getCy: function () {
      return null;
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
    deleteItemConfirm() {
      this.elements.splice(this.editedIndex, 1);
      this.close();
      this.closeDelete();
    },
    addEdgesToObject(edge) {
      this.elements = [...this.elements, edge];
    },
    addNode() {
      // console.log("This is cy ref",this.$refs.cyRef.cy)
      console.log("Edited index is", this.editedIndex);
      if (this.editedIndex == -1) {
        //add new node {
        const nextNode = {
          data: { id: this.nodeDetails.node_name },
          position: {
            x: this.nodeDetails.x_point,
            y: this.nodeDetails.y_point,
          },
          group: "nodes",
          selected: this.nodeDetails.selected,
          selectable: this.nodeDetails.selectable,
          locked: this.nodeDetails.locked,
          grabbable: this.nodeDetails.grabbable,
          pannable: this.nodeDetails.pannable,
        };
        this.elements = [...this.elements, nextNode];
      } else {
        let element = this.elements[this.editedIndex];
        console.log("The original element is", JSON.stringify(element));
        element.data.id = this.nodeDetails.node_name;
        element.selected= this.nodeDetails.selected;
        element.selectable= this.nodeDetails.selectable;
        element.locked= this.nodeDetails.locked;
        element.grabbable= this.nodeDetails.grabbable;
        element.pannable= this.nodeDetails.pannable;
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
        selected: this.defaultItem.selected,
        selectable: this.defaultItem.selectable,
        locked: this.defaultItem.locked,
        grabbable: this.defaultItem.grabbable,
        pannable: this.defaultItem.pannable
      };
      if (event.target === this.$refs.cyRef.instance) {
        this.nodeDetails.x_point = event.originalEvent.layerX;
        this.nodeDetails.y_point = event.originalEvent.layerY;
        this.nodeDetails.selected = this.defaultItem.selected;
        this.nodeDetails.selectable = this.defaultItem.selectable;
        this.nodeDetails.locked = this.defaultItem.locked;
        this.nodeDetails.grabbable = this.defaultItem.grabbable;
        this.nodeDetails.pannable = this.defaultItem.pannable;
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
      this.nodeDetails.selected = node.selected != undefined ? node.selected : this.defaultItem.selected;
      this.nodeDetails.selectable = node.selectable != undefined ? node.selectable: this.defaultItem.selectable;
      this.nodeDetails.locked = node.locked != undefined ? node.locked : this.defaultItem.locked;
      this.nodeDetails.grabbable = node.grabbable != undefined ? node.grabbable : this.defaultItem.grabbable;
      this.nodeDetails.pannable = node.pannable != undefined ? node.pannable : this.defaultItem.pannable;
      this.editedIndex = this.elements.indexOf(node);
      this.nodeDetails = Object.assign({}, this.nodeDetails);
      this.dialog = true;
    },
    deleteGraphNode(id) {
      let node = this.elements.find((x) => x.data.id == id);
      this.editedIndex = this.elements.indexOf(node);
      this.dialogDelete = true;
      console.log(id)
    },
    deleteNode(id) {
      console.log("node clicked", id);
    },
    updateNode(event) {
      
      console.log("right click node", event);
    },
    drawModeToggle() {
      this.isDrawMode = !this.isDrawMode;
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
          console.log(sourceNode.data().id)
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
          console.log('After adding edges',JSON.stringify(this.elements));   

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
      console.log("EH is",eh);


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
  // data: () => ({
  //   ecosystem: [
  //     {
  //       text: 'vuetify-loader',
  //       href: 'https://github.com/vuetifyjs/vuetify-loader',
  //     },
  //     {
  //       text: 'github',
  //       href: 'https://github.com/vuetifyjs/vuetify',
  //     },
  //     {
  //       text: 'awesome-vuetify',
  //       href: 'https://github.com/vuetifyjs/awesome-vuetify',
  //     },
  //   ],
  //   importantLinks: [
  //     {
  //       text: 'Documentation',
  //       href: 'https://vuetifyjs.com',
  //     },
  //     {
  //       text: 'Chat',
  //       href: 'https://community.vuetifyjs.com',
  //     },
  //     {
  //       text: 'Made with Vuetify',
  //       href: 'https://madewithvuejs.com/vuetify',
  //     },
  //     {
  //       text: 'Twitter',
  //       href: 'https://twitter.com/vuetifyjs',
  //     },
  //     {
  //       text: 'Articles',
  //       href: 'https://medium.com/vuetify',
  //     },
  //   ],
  //   whatsNext: [
  //     {
  //       text: 'Explore components',
  //       href: 'https://vuetifyjs.com/components/api-explorer',
  //     },
  //     {
  //       text: 'Select a layout',
  //       href: 'https://vuetifyjs.com/getting-started/pre-made-layouts',
  //     },
  //     {
  //       text: 'Frequently Asked Questions',
  //       href: 'https://vuetifyjs.com/getting-started/frequently-asked-questions',
  //     },
  //   ],
  // }),
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
