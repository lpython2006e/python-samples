from itemadapter import ItemAdapter


class LivestockclawlingPipeline:
    def process_item(self, item, spider):
        # switch case
        item.save()
        return item
