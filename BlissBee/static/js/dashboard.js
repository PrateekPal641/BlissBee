let emotion = ['Shock', 'Confusion', 'Guilt', 'Rejection', 'Anger', 'Despair'],
	 shock = 'Shock',
   confusion = 'Confusion',
   guilt = 'Guilt',
   rejection = 'Rejection',
   anger = 'Anger',
   despair = 'Despair';
function chooseWisely() {
	$.each(emotion, function(index, value) {
  		$('#outer-ring-inner').append(`<div class="emotion-ball">${value}</div>`);
	});
	$('#outer-ring-inner > div:nth-child(1)').addClass('current-emotion-shock');
	$('.emotion-ball').on('click', function  () {
		if($(this).text().match(shock)) {
      $('.emotion-ball').removeClass('current-emotion-confusion current-emotion-guilt current-emotion-rejection current-emotion-anger current-emotion-despair');
			$(this).addClass('current-emotion-shock');
			$('.response').html('<div class="response-inner-wrapper"><div class="response-inner"><p>“I feel numb”</p><p>Feelings of being dazed or detached are common responses to a suicide. At first, shock can protect you from feeling overwhelmed.</p></div><div id="response-shock-border"></div></div>');
		} 
    if($(this).text().match(anger)) {
			$('.emotion-ball').removeClass('current-emotion-shock current-emotion-confusion current-emotion-guilt current-emotion-rejection current-emotion-despair');
			$(this).addClass('current-emotion-anger');
      $('.response').removeClass('shock-response').html('<div class="response-inner-wrapper"><div class="response-inner"><p>“How could they do this to me?”</p><p>You might feel like your loved one abandoned you, or be angry for missing warning signs.</p></div><div id="response-anger-border"></div></div>');
    }
    if($(this).text().match(guilt)) {
      $('.emotion-ball').removeClass('current-emotion-shock current-emotion-confusion current-emotion-rejection current-emotion-anger current-emotion-despair');
			$(this).addClass('current-emotion-guilt');
			$('.response').html('<div class="response-inner-wrapper"><div class="response-inner"><p>“I should have done more”</p><p>You might replay “what if” and “if only” scenarios in your mind. You may also feel regret about things said or not said.</p></div><div id="response-guilt-border"></div></div>');
    }
    if($(this).text().match(despair)) {
      $('.emotion-ball').removeClass('current-emotion-shock current-emotion-confusion current-emotion-rejection current-emotion-anger current-emotion-guilt');
			$(this).addClass('current-emotion-despair');
$('.response').html('<div class="response-inner-wrapper"><div class="response-inner"><p>“Why bother”</p><p>You might be gripped by sadness, loneliness or helplessness. You might have a physical collapse or even consider suicide yourself.</p></div><div id="response-despair-border"></div></div>');
    }
    if($(this).text().match(confusion)) {
      $('.emotion-ball').removeClass('current-emotion-shock current-emotion-guilt current-emotion-rejection current-emotion-anger current-emotion-despair');
			$(this).addClass('current-emotion-confusion');
			$('.response').html('<div class="response-inner-wrapper"><div class="response-inner"><p>“I just don’t understand why”</p><p>Many people try to make some sense out of the death, or try to understand why their loved one took his or her life.</p></div><div id="response-confusion-border"></div></div>');
    }
    if($(this).text().match(rejection)) {
      $('.emotion-ball').removeClass('current-emotion-shock current-emotion-confusion current-emotion-guilt current-emotion-anger current-emotion-despair');
			$(this).addClass('current-emotion-rejection');
			$('.response').html('<div class="response-inner-wrapper"><div class="response-inner"><p>“Why wasn’t I enough?”</p><p>You might wonder why your relationship wasn’t enough to keep your loved one from taking his or her life.</p></div><div id="response-rejection-border"></div></div>');
    }
	});
}

chooseWisely();

