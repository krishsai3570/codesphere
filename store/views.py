from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import View,FormView,CreateView,TemplateView

from store.forms import SignUpForm,SignInForm,UserProfileForm,ProjectForm

from django.contrib.auth import authenticate,login,logout

from store.models import Project,WishListItem

from django.contrib import messages

from django.db.models import Sum



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






class IndexView(View):



    template_name="index.html"  

    def get(self,request,*args,**kwrags):

        qs=Project.objects.all().exclude(developer=request.user)

        return render(request,self.template_name,{"data":qs})  
    


class LogOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("sign-in")

    
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



class MyProjectListView(View):

    template_name="project_list.html"



    def get(self,request,*args,**kwargs):

        qs=Project.objects.filter(developer=request.user)

        return render(request,self.template_name,{"data":qs})

    

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
    


class ProjectDetailView(View):

    template_name="project_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Project.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})
    






   
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

    


