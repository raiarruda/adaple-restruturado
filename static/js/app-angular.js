var app = angular.module('adalin', []);
app.controller('adalinRecursosController', function($scope, $http){
     $scope.todoList = [{todoText: 'Terminar esse app', done: false}]


     $scope.get = function (response) {
        $scope.todoList = [];
   
            var todo = {};
            todo.todoText = $scope.text

            todo.done = $scope.done
            todo.id = $scope.id
            
        
       
   };

     $scope.todoAdd = function(){
        $scope.todoList.push({todoText: $scope.todoInput, done: false});
        $scope.todoInput = '';

    };

   
    $http.salvar = function(){
        var data = {nome:$scope.video}
        $http.put('/edps/video/api/', data)
    };

})