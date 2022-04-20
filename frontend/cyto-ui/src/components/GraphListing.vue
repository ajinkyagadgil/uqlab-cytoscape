<template>
  <v-data-table
    :headers="headers"
    :items="graphs[0].data"
    sort-by="calories"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>All Graphs</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
              New Graph
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <!-- <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.graph_id"
                      label="Graoh Id"
                    ></v-text-field>
                  </v-col> -->
                  <v-col>
                    <v-text-field
                      v-model="editedItem.graph_name"
                      label="Graph Name"
                    ></v-text-field>
                  </v-col>
                  <!-- <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.fat"
                      label="Fat (g)"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.carbs"
                      label="Carbs (g)"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.protein"
                      label="Protein (g)"
                    ></v-text-field>
                  </v-col> -->
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
            
              <v-btn color="blue darken-1" text @click="close"> Cancel </v-btn>
              <v-btn color="blue darken-1" text @click="save"> Save </v-btn>
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
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
      <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize"> Reset </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    dialog: false,
    dialogDelete: false,
    headers: [
      { text: "Graph Name", value: "attributes.Name" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    desserts: [],
    graphs: [],
    editedIndex: -1,
    editedItem: {
      // graph_id: "",
      graph_name: "",
      // fat: 0,
      // carbs: 0,
      // protein: 0,
    },
    defaultItem: {
      // graph_id: "",
      graph_name: "",
      // name: "",
      // calories: 0,
      // fat: 0,
      // carbs: 0,
      // protein: 0,
    },
  }),
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Graph" : "Edit Graph";
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
    editItem(item) {
      this.$router.push({ name: "Graph", params: { id: item.id } });
    },

    deleteItem(item) {
      this.editedIndex = this.graphs[0].data.indexOf(item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      let graphToDelete = this.graphs[0].data[this.editedIndex];
      axios
        .delete(`http://localhost:1337/api/graphs/${graphToDelete.id}`)
        .then((response) => {
          if (response.status == 200) {
            this.graphs[0].data.splice(this.editedIndex, 1);
          }
        });
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    async save() {
      const graphNameCreate = {
        data: {
          Name: this.editedItem.graph_name,
        },
      };
      // console.log(JSON.stringify(data))
      axios
        .post("http://localhost:1337/api/graphs", graphNameCreate)
        .then((response) => {
          if (response.status == 200) {
            console.log("The response is", response.data.data.id);
            this.$router.push({ name: "Graph", params: { id: response.data.data.id } });
          }
        });
      // if (this.editedIndex > -1) {
      //   Object.assign(this.desserts[this.editedIndex], this.editedItem);
      // } else {
      //   this.desserts.push(this.editedItem);
      // }
      const { graphData } = await this.fetchData();
      // console.log("The id created is", graphData)
      this.graphs.push(graphData);
      // this.graphs = [...this.graphs, graphData];
      this.close();
    },

    async fetchData() {
      const res = await fetch("http://localhost:1337/api/graphs");
      return res.json();
    },
  },
  async created() {
    //this.initialize();
    const graphData = await this.fetchData();
    this.graphs = [...this.graphs, graphData];
  },
};
</script>

<style scoped>
</style>