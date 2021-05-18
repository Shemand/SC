<template>
    <div ref="computers_table" style='height: 1900px; wight: 1000px;'></div>
</template>

<script>
import GetRequestsMixin from "@/mixins/GetRequestsMixin.js"
import Tabulator from "tabulator-tables"
export default {
    mixins : [GetRequestsMixin],
    data() {
        return {
            tableData: [],
            tableRef: null,
            tabulator: undefined,
        }
    },
//    watch : {
//        tableData: {
//            handler: function(newData) {
//                this.tabulator.replaceData(newData)
//            },
//            deep: true,
//        }
//    },
    mounted() {
        console.log(this.$refs.computers_table)
        this.tabulator = new Tabulator(this.$refs.computers_table, {
            data: this.tableData,
            layout: "filColumns",
            tooltips: true,
            pagination:"local",
            index: "name",
            paginationSize: 100,
            initialSort:[
                {column:"name", dir:"asc"},
            ],
            reactiveData: true,
            columns: [
                {title:"№", hozAlign:"center", formatter : "rownum", width:49, sorter:false, editor:false},
                {title:"Имя компьютера", field:"name", hozAlign:"center", sorter:"string", headerFilter:true}
            ],
        })
        this.tableData = []
        let context = this
        context.getComputers().then(function(computers){
            console.log(computers)
            computers.forEach(function(computer){
                context.tableData.push({
                    name: computer.name
                })
            });
            context.tabulator.replaceData(context.tableData)
       });
    }
}
</script>

<style lang="scss" scoped>
  @import  "~tabulator-tables/dist/css/bootstrap/tabulator_bootstrap";
</style>
