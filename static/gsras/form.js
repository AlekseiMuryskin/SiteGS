$(document).ready (function () {
        $("[name = choice_data_type]").on ("change", function  () {
            if (this.value == 'retro'){
                $("#switch_text").html ("Вложение со списком запрашиваемых материалов *");
            }
            else if (this.value = 'realtime'){
               $("#switch_text").html ("Вложение со списком запрашиваемых станций *");
            }
        })
    })