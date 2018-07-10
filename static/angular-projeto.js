var app = angular.module('projeto', []);
app.controller('projetoController', function($scope, $http){
    // $scope.todoList = [{todoText: 'Terminar esse app', done: false}]
   $http.get('/edps/edps/api/').then(function (response) {
        $scope.edpLista = [];
        for (var i = 0; i < response.data.length; i++) {

            var edp = {};
            edp.titulo = response.data[i].titulo
            edp.slug = response.data[i].slug
            edp.objetivo_pedagogico = response.data[i].objetivo_pedagogico
            edp.habilidades = response.data[i].habilidades
            edp.atividades = response.data[i].atividades
            edp.metodologia = response.data[i].metodologia
            edp.usuario = response.data[i].usuario
            edp.nivel = response.data[i].nivel
            $scope.edpLista.push(edp);
          }
       
   });

   $scope.saveData = function(){
       var data = {text: $scope.todoInput, done:false}
       $http.put('/projeto/api/', data)
   }

    $scope.todoAdd = function(){
        $scope.todoList.push({todoText: $scope.todoInput, done: false});
        $scope.todoInput = '';
    };



    $scope.remove = function () {
        var oldList = $scope.todoList;
        $scope.todoList = [];
        angular.forEach(oldList, function(todo) {
            if(todo.done){
                $http.delete('/projeto/api/' + todo.id +'/');
            } 
            else {
                $scope.todoList.push(todo);
            }
        })
       
    }
})