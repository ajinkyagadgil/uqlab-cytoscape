<template>
  <div id="hello">
    <div id="cyto" ref="cyto">
      <!-- <button id="draw-on" style="color: red">Draw mode on</button>
    <button id="draw-off" @click="saveData()">Save</button> -->
      <cytoscape
        ref="cyRef"
        :config="config"
        v-on:mousedown="addNodeDetails"
        v-on:cxttapstart="updateNode"
        :preConfig="preConfig"
        :afterCreated="afterCreated"
      >
        <cy-element
          v-for="def in elements"
          :key="`${def.data.id}`"
          :definition="def"
          v-on:mousedown="addEdges(def.data.id)"
        />
        <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="text-h5">Add Node</span>
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
                      required
                      @change="$v.checkbox.$touch()"
                      @blur="$v.checkbox.$touch()"
                    ></v-checkbox>
                  </v-col>
                  <v-col>
                    <v-checkbox
                      v-model="nodeDetails.selectable"
                      label="Selectable"
                      required
                      @change="$v.checkbox.$touch()"
                      @blur="$v.checkbox.$touch()"
                    ></v-checkbox>
                  </v-col>
                  <v-col>
                    <v-checkbox
                      v-model="nodeDetails.locked"
                      label="Locked"
                      required
                      @change="$v.checkbox.$touch()"
                      @blur="$v.checkbox.$touch()"
                    ></v-checkbox>
                  </v-col>
                  <v-col>
                    <v-checkbox
                      v-model="nodeDetails.grabbable"
                      label="Grabbable"
                      required
                      @change="$v.checkbox.$touch()"
                      @blur="$v.checkbox.$touch()"
                    ></v-checkbox>
                  </v-col>
                  <v-col>
                    <v-checkbox
                      v-model="nodeDetails.pannable"
                      label="Pannable"
                      required
                      @change="$v.checkbox.$touch()"
                      @blur="$v.checkbox.$touch()"
                    ></v-checkbox>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close"> Cancel </v-btn>
              <v-btn color="blue darken-1" text @click="addNode">
                Add Node
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </cytoscape>
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
import jquery from "jquery";
import contextMenus from "cytoscape-context-menus";
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
      config,
      elements,
      isDrawMode: false,
      json1_data: "",
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
  watch: {
    dialog(val) {
      val || this.close();
    },
  },
  methods: {
    getCy: function () {
      return null;
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    addNode() {
      // console.log("This is cy ref",this.$refs.cyRef.cy)
      const nextNode = {
        data: { id: this.nodeDetails.node_name },
        position: { x: this.nodeDetails.x_point, y: this.nodeDetails.y_point },
        group: "nodes",
        selected: this.nodeDetails.selected,
        selectable: this.nodeDetails.selectable,
        locked: this.nodeDetails.locked,
        grabbable: this.nodeDetails.grabbable,
        pannable: this.nodeDetails.pannable,
      };
      let cy = this.getCy();
      //cy.add(nextNode)
      this.elements = [...this.elements, nextNode];
      console.log("The cy obj is", cy);
      console.log(nextNode);
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
      };
      if (event.target === this.$refs.cyRef.instance) {
        this.nodeDetails.x_point = event.originalEvent.layerX;
        this.nodeDetails.y_point = event.originalEvent.layerY;
        this.dialog = true;

        // console.log(event.originalEvent.layerX);
        // console.log(event.originalEvent.layerY);
        // console.log(event.target, this.$refs.cyRef.instance);
        // const newNode = {
        //   data: { id: "d" },
        //   position: { x: 489, y: 400 },
        //   group: "nodes",
        // };
        // //test node for cy event
        // const nextNode = {
        //   data: { id: "e" },
        //   position: { x: 490, y: 450 },
        //   group: "nodes",
        // };
        // event.cy.add(nextNode);
        // event.cy.add(newNode);
        // console.log("Event data is", event.cy.data());
        // console.log("cy is", event.cy);
        // this.elements = [...this.elements, newNode];
        // console.log("adding node", event.target);
        // this.saveChanges(event.cy);
      }
    },
    saveData() {
      const s = this.json1_data;

      const dataToSave = {
        data: {
          Graph_Id: "graph110",
          Name: "graph 110",
          data: s,
        },
      };
      // console.log(JSON.stringify(data))
      axios
        .post("http://localhost:1337/api/graphs", dataToSave)
        .then((response) => {
          console.log(response);
        });
    },
    saveChanges(cy) {
      console.log("The cy in save changes is", cy.json()["elements"]);
      console.log(
        "JSON data in save changes",
        JSON.stringify(cy.json()["elements"])
      );
      this.json1_data = cy.json()["elements"];
    },
    addEdges(id) {
      console.log("node click", id);
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
    preConfig(cytoscape) {
      if (!cytoscape("core", "contextMenus")) {
        //cytoscape.use(cxtmenu);
        contextMenus(cytoscape, jquery);
        edgehandles(cytoscape);
      }

      // cytoscape.use(edgehandles);
      console.log("calling pre-config", cytoscape);
    },
    afterCreated(cy) {
      console.log("After created called");
      // cy: this is the cytoscape instance
      console.log("after created", cy);
      cy.contextMenus({
        menuItems: [
          {
            id: "remove",
            content: "remove",
            tooltipText: "remove",
            image: { src: "remove.svg", width: 12, height: 12, x: 6, y: 4 },
            selector: "node, edge",
            onClickFunction: function (event) {
              var target = event.target || event.cyTarget;
              target.remove();
            },
            hasTrailingDivider: true,
          },
          {
            id: "hide",
            content: "hide",
            tooltipText: "hide",
            selector: "*",
            onClickFunction: function (event) {
              var target = event.target || event.cyTarget;
              target.hide();
            },
            disabled: false,
          },
        ],
      });
      var eh = cy.edgehandles({
        canConnect: function (sourceNode, targetNode) {
          // whether an edge can be created between source and target
          return !sourceNode.same(targetNode); // e.g. disallow loops
        },
        edgeParams: function (sourceNode, targetNode) {
          console.log("Soure node is", sourceNode);
          console.log("Dest node is", targetNode);
          console.log("This is cy", cy);
          // for edges between the specified source and target
          // return element object to be passed to cy.add() for edge

          // const newEdge = {
          //   data: {
          //     id: sourceNode + targetNode,
          //     source: sourceNode,
          //     target: targetNode,
          //   },
          //   group:"edges"
          // };
          // cy.add(newEdge)
          // this.saveChanges()
          return {};
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
      console.log(eh);
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
