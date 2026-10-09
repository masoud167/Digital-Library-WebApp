import os
from collections import Counter

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404

from .models import Book, Category, BorrowRecord, Review


def _child_map():
    """نقشه شناسه والد -> شناسه‌های فرزندان برای پیمایش درختی دسته‌ها"""
    mapping = {}
    for cid, pid in Category.objects.values_list('id', 'parent_id'):
        mapping.setdefault(pid, []).append(cid)
    return mapping


def _category_tree_ids(category, child_map):
    """شناسه‌های خود دسته + همه زیردسته‌های آن"""
    ids = {category.pk}
    stack = [category.pk]
    while stack:
        for child in child_map.get(stack.pop(), ()):
            if child not in ids:
                ids.add(child)
                stack.append(child)
    return ids


def book_list(request):
    books = Book.objects.all().order_by('-created_at')

    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    direct_counts = Counter(books.values_list('category_id', flat=True))
    category_map = _child_map()

    categories = list(
        Category.objects.filter(parent__isnull=True).prefetch_related('children')
    )
    for cat in categories:
        cat.total_books = sum(
            direct_counts.get(cid, 0) for cid in _category_tree_ids(cat, category_map)
        )
        for sub in cat.children.all():
            sub.total_books = direct_counts.get(sub.pk, 0)

    slugs = request.GET.getlist('category')
    by_slug = (
        {c.slug: c for c in Category.objects.filter(slug__in=slugs)} if slugs else {}
    )
    selected_categories = [by_slug[s] for s in slugs if s in by_slug]
    selected_slugs = [s for s in slugs if s in by_slug]

    if selected_categories:
        tree_ids = set()
        for selected in selected_categories:
            tree_ids |= _category_tree_ids(selected, category_map)
        books = books.filter(category_id__in=tree_ids)

    context = {
        'books': books,
        'categories': categories,
        'selected_categories': selected_categories,
        'selected_slugs': selected_slugs,
        'query': query,
    }
    return render(request, 'books/book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()  
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        rating = request.POST.get('rating')
        comment_text = request.POST.get('comment')

        if rating and comment_text:
            Review.objects.update_or_create(
                book=book,
                user=request.user,
                defaults={
                    'rating': int(rating),
                    'comment': comment_text
                }
            )
            return redirect('books:book_detail', pk=book.pk)

    context = {
        'book': book,
        'reviews': reviews,
    }
    return render(request, 'books/book_detail.html', context)


@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    BorrowRecord.objects.get_or_create(
        user=request.user,
        book=book
    )

    if book.pdf_file and os.path.exists(book.pdf_file.path):
        return FileResponse(
            open(book.pdf_file.path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(book.pdf_file.name),
        )
    return redirect('books:book_detail', pk=pk)


@login_required
def download_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if not BorrowRecord.objects.filter(user=request.user, book=book).exists():
        raise Http404("سابقه امانتی برای شما ثبت نشده است")

    if book.pdf_file and os.path.exists(book.pdf_file.path):
        return FileResponse(
            open(book.pdf_file.path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(book.pdf_file.name),
        )
    return redirect('books:book_detail', pk=pk)
