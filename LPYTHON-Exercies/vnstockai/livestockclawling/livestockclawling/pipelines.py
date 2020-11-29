from itemadapter import ItemAdapter


class LivestockclawlingPipeline:
    def process_item(self, item, spider):
        # switch case
        test=id(item)
        item.save()
        return item
