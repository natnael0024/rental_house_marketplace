from django.shortcuts import render, get_object_or_404, redirect
from.models import Conversation, Message
from users.models import CustomUser

def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user)
    
    for conversation in conversations:
        other_participant = None
        for participant in conversation.participants.all():
            if participant != request.user:
                other_participant = participant
                break

    return render(request, 'messaging/conversation_list.html', {'conversations': conversations, 'other_participant':other_participant})

def start_conversation(request, user_id):
    other_user = get_object_or_404(CustomUser, pk=user_id)
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    return redirect('conversation_detail', pk=conversation.pk)

def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    messages = Message.objects.filter(conversation=conversation).order_by('created_at')
    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation, 'messages': messages})

def send_message(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    message = Message.objects.create(author=request.user, conversation=conversation, content=request.POST.get('content'))
    return redirect('conversation_detail', pk=conversation.pk)
