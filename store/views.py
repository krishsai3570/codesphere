from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import View,FormView,CreateView,TemplateView

from store.forms import SignUpForm,SignInForm,UserProfileForm,ProjectForm,PasswordResetForm

from django.contrib.auth import authenticate,login,logout

from store.models import Project,WishListItem,Order

from django.contrib import messages

from django.db.models import Sum

from django.views.decorators.csrf import csrf_exempt 

from django.utils.decorators import method_decorator

from django.core.mail import send_mail

from store.decorators import signin_required
from django.views.decorators.cache import never_cache

from django.contrib.auth.models import User



def send_email():
    send_mail(
    "Code hub project dwnld",
    "you have completed purshace of project.",
    "krishsai3570@gmail.com",
    ["krishsai0700@gmail.com"],
    fail_silently=False,
)



class SignUpView(CreateView):

   
    template_name="register.html"

    form_class=SignUpForm

    success_url=reverse_lazy("sign-in")

    # def get(self,request,*args,**kwargs):

    #     form_instance=self.form_class()

    #     return render(request,self.template_name,{"form":form_instance})
            

    # def post(self,request,*args,**kwargs):

    #     form_instance=self.form_class(request.POST)

    #     if form_instance.is_valid:

    #         form_instance.save()

    #         print("account created")

    #         return redirect("sign-up")
        
    #     else:
    #         return render(request,self.template_name,{"form":form_instance})



class SignInView(FormView):

    template_name="login.html"  

    form_class=SignInForm


    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            username=form_instance.cleaned_data.get("username")

            pwd=form_instance.cleaned_data.get("password")

            user_object=authenticate(username=username,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("index")
            
        return render(request,self.template_name,{"form":form_instance})







@method_decorator([signin_required,never_cache],name="dispatch")
class IndexView(View):

    template_name="index.html"  

    def get(self,request,*args,**kwrags):

        qs=Project.objects.all().exclude(developer=request.user)

        return render(request,self.template_name,{"data":qs})  
    


class LogOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("sign-in")




@method_decorator([signin_required,never_cache],name="dispatch")   
class UserProfileEditView(View):

    template_name="profile_edit.html"


    form_class=UserProfileForm

    def get(self,request,*args,**kwargs):

        user_profile_instance=request.user.profile

        form_instance=self.form_class(instance=user_profile_instance)

        return render(request,self.template_name,{"form":form_instance})
        

    def post(self,request,*args,**kwargs):

        user_profile_instance=request.user.profile

        form_instance=self.form_class(request.POST,instance=user_profile_instance,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("index")
        
        else:
            return render(request,self.template_name,{"form":form_instance})
        



@method_decorator([signin_required,never_cache],name="dispatch")
class ProjectAddView(View):
    
    template_name="project_add.html"

    form_class=ProjectForm


    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()


        return render(request,self.template_name,{"form":form_instance})



    def post(self,request,*args,**kwrags):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            form_instance.instance.developer=request.user

            form_instance.save()

            return redirect("index")
        else:
           
            return render(request,self.template_name,{"form":form_instance})





@method_decorator([signin_required,never_cache],name="dispatch")
class MyProjectListView(View):

    template_name="project_list.html"



    def get(self,request,*args,**kwargs):

        qs=Project.objects.filter(developer=request.user)

        return render(request,self.template_name,{"data":qs})




    
@method_decorator([signin_required,never_cache],name="dispatch")
class MyprojectUpdateView(View):

    template_name="project_update.html"

    form_class=ProjectForm


    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")    

        project_object=Project.objects.get(id=id)

        form_instance=self.form_class(instance=project_object)

        return render(request,self.template_name,{"form":form_instance})
    


    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Project_object=Project.objects.get(id=id)

        form_instance=self.form_class(request.POST,instance=Project_object,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("myworks-all")
        else:
            return render(request,self.template_name,{"form":form_instance})
    

@method_decorator([signin_required,never_cache],name="dispatch")
class ProjectDetailView(View):

    template_name="project_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Project.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})
    






@method_decorator([signin_required,never_cache],name="dispatch")  
class AddToWishListView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        #project_onject=Project.objects.get(id=id)

        project_object=get_object_or_404(Project,id=id)

        try:

            request.user.basket.basket_item.create(project_object=project_object)
            messages.success(request,"item has been added")

        except Exception as e:
            messages.error(request,"failed to add")

        return redirect("index")






@method_decorator([signin_required,never_cache],name="dispatch")
class WishListView(View):

    template_name="wishlist.html"

    def get(self,request,*args,**kwargs):

        
        qs=request.user.basket.basket_item.filter(is_order_placed=False)
        
        total=qs.values("project_object").aggregate(total=Sum("project_object__price")).get("total")
      
        return render(request,self.template_name,{"data":qs,"total":total})

        
 

    
class WishListItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        WishListItem.objects.get(id=id).delete()

        return redirect("add-to-wish")

    

import razorpay
@method_decorator([signin_required,never_cache],name="dispatch")
class CheckOutView(View):

    template_name="check_out.html"
    def get(self,request,*args,**kwargs):

        KEY_ID="rzp_test_bSgPSgM6pYLVno"
        KET_SECRET="zSuIh5beN9zbYsuRYO9cSZYl"


        client = razorpay.Client(auth=(KEY_ID,KET_SECRET))

        amount=request.user.basket.basket_item.filter(is_order_placed=False).values("project_object").aggregate(total=Sum("project_object__price")).get("total")

        data = { "amount": amount*100, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

        order_id=payment.get("id")

        order_object=Order.objects.create(order_id=order_id,costumer=request.user)

        wishlist_items=request.user.basket.basket_item.filter(is_order_placed=False)

        for wi in wishlist_items:

            order_object.wishlist_item_objects.add(wi)

            wi.is_order_placed=True

            wi.save()




        return render(request,self.template_name,{"key_id":KEY_ID,"amount":amount,"order_id":order_id})


      

@method_decorator([signin_required,never_cache],name="dispatch")
@method_decorator(csrf_exempt,name="dispatch") 
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        KEY_ID="rzp_test_bSgPSgM6pYLVno"
        KET_SECRET="zSuIh5beN9zbYsuRYO9cSZYl"

        client=razorpay.Client(auth=(KEY_ID,KET_SECRET))

        try:
            client.utility.verify_payment_signature(request.POST)

            order_id=request.POST.get("razorpay_order_id")

            Order.objects.filter(order_id=order_id).update(is_paid=True)

            send_email()


            print("success")

        except:

            print("failed")

        return redirect("orders")



# my order view
@method_decorator([signin_required,never_cache],name="dispatch")
class MyOrdersView(View):

    template_name="myorders.html"

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(costumer=request.user)

        return render(request,self.template_name,{"data":qs})
    




class PasswordResetView(View):

    template_name="password_reset.html"

    form_class=PasswordResetForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            username=form_instance.cleaned_data.get("username")

            email=form_instance.cleaned_data.get("email")

            password1=form_instance.cleaned_data.get("password1")

            password2=form_instance.cleaned_data.get("password2")

            print(username,email,password1,password2)

            try:

                assert password1==password2,("password mismatch")

                user_object=User.objects.get(username=username,email=email)
                user_object.set_password(password2)

                user_object.save()

             


                return redirect("sign-in")
        
            except Exception as e:

                messages.error(request,f"{e}")
                return render(request,self.template_name,{"form":form_instance})
        

        else:

            return render(request,self.template_name,{"form":form_instance})
        

            
