import qs from 'qs'
export default {
  methods: {
      getComputers : function() {
          return this.$http({
              url : "/api/v1/SZO/computers?puppet=[]&kaspersky=[]&dallas_lock=[]&active_directory=[]",
              method : 'GET',
//              data: qs.stringify({
//                puppet: [],
//                kaspersky: [],
//                dallas: [],
//                active_directory: []
//              }),
              headers: {
                'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
              },
              withCredentials : true
          }).then(function(res) {
              return res.data.data.computers
          }).catch(function(err) {
              return []
          });
      }
  }
}