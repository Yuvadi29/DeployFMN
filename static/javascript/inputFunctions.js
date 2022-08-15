function wordCounter(input_value,max_letters){
    input_value_length = input_value.value.length;
    document.getElementById("input_length_counter").textContent = input_value_length;

    if(input_value_length > max_letters){
        document.getElementById("input_length_counter").classList.add('imp-field')
    }
    else if(input_value_length <= max_letters){
        document.getElementById("input_length_counter").classList.remove('imp-field')
    }
}
console.log("Connected")